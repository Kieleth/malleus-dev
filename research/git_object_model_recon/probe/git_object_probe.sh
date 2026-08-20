#!/bin/bash
# Empirical probe of git's object database, for a recon record.
# Deterministic: fixed identity, fixed dates.
set -u
export GIT_AUTHOR_NAME=R GIT_AUTHOR_EMAIL=r@x GIT_COMMITTER_NAME=R GIT_COMMITTER_EMAIL=r@x
export GIT_AUTHOR_DATE="2020-01-01T00:00:00+0000" GIT_COMMITTER_DATE="2020-01-01T00:00:00+0000"
W=$(mktemp -d)
cd "$W" || exit 1

echo "##### A. object name is a pure function of (type, length, bytes)"
mkdir a && cd a && git init -q .
printf 'hello\n' > f.txt
BLOB=$(git hash-object -w f.txt)
echo "git hash-object     : $BLOB"
MANUAL=$(printf 'blob 6\0hello\n' | shasum -a 1 | cut -d' ' -f1)
echo "sha1('blob 6\\0hello'): $MANUAL"
echo "empty blob          : $(printf '' | git hash-object --stdin)"
echo "same bytes, other name:"
cp f.txt g.txt; echo "  g.txt -> $(git hash-object g.txt)"
echo "raw object file on disk:"
ls .git/objects/${BLOB:0:2}/
echo "loose object is zlib of the same preimage:"
python3 -c "
import zlib,sys
d=open('.git/objects/${BLOB:0:2}/${BLOB:2}','rb').read()
print('  inflated =', repr(zlib.decompress(d)))
"

echo
echo "##### B. two independent repos, same content -> same blob AND same tree, different commit"
cd "$W"; mkdir r1 r2
for r in r1 r2; do
  cd "$W/$r" && git init -q .
  # r1 reaches the state in 1 commit, r2 in 3 commits by a different route
  if [ "$r" = r1 ]; then
    printf 'alpha\n' > a.txt; printf 'beta\n' > b.txt
    git add . && git commit -qm one
  else
    printf 'WRONG\n' > a.txt; git add . && git commit -qm x
    printf 'alpha\n' > a.txt; git add . && git commit -qm y
    printf 'beta\n'  > b.txt; git add . && git commit -qm z
  fi
done
echo "r1 tree  : $(cd $W/r1 && git rev-parse HEAD^{tree})   commit: $(cd $W/r1 && git rev-parse HEAD)"
echo "r2 tree  : $(cd $W/r2 && git rev-parse HEAD^{tree})   commit: $(cd $W/r2 && git rev-parse HEAD)"
echo "r1 a.txt blob: $(cd $W/r1 && git rev-parse HEAD:a.txt)"
echo "r2 a.txt blob: $(cd $W/r2 && git rev-parse HEAD:a.txt)"
echo "r1 commit object body:"
(cd $W/r1 && git cat-file -p HEAD) | sed 's/^/    /'
echo "r2 commit object body:"
(cd $W/r2 && git cat-file -p HEAD) | sed 's/^/    /'
echo "r1 tree object body:"
(cd $W/r1 && git cat-file -p HEAD^{tree}) | sed 's/^/    /'

echo
echo "##### C. divergence and re-convergence inside one repo"
cd "$W"; mkdir c && cd c && git init -q .
printf 'base\n' > s.txt; git add .; git commit -qm base
BASE=$(git rev-parse HEAD)
git checkout -q -b left;  printf 'X\n' >> s.txt; git add .; git commit -qm left
git checkout -q $BASE -b right2 2>/dev/null; git checkout -q -B right $BASE
printf 'X\n' >> s.txt; git add .; git commit -qm right-different-message
echo "left  : commit $(git rev-parse left)  tree $(git rev-parse left^{tree})"
echo "right : commit $(git rev-parse right) tree $(git rev-parse right^{tree})"
echo "-> identical content on two branches: trees converge, commits do not."
echo "object count in this repo (all four objects for one file state, shared):"
git count-objects -v

echo
echo "##### D. packing and deltas"
cd "$W"; mkdir p && cd p && git init -q .
python3 - <<'PY'
import random
random.seed(7)
lines=[f"line {i} lorem ipsum dolor sit amet consectetur\n" for i in range(4000)]
open("big.txt","w").writelines(lines)
PY
git add . ; git commit -qm v1
for i in $(seq 1 30); do
  python3 - "$i" <<'PY'
import sys
i=int(sys.argv[1])
ls=open("big.txt").readlines()
ls[i*7] = f"CHANGED at revision {i}\n"
open("big.txt","w").writelines(ls)
PY
  git add . ; git commit -qm "v$((i+1))"
done
echo "loose object store before gc:"
git count-objects -v -H
du -sh .git/objects 2>/dev/null | sed 's/^/  du: /'
git gc -q 2>/dev/null
echo "after gc:"
git count-objects -v -H
du -sh .git/objects | sed 's/^/  du: /'
echo "delta chains (verify-pack, blobs only, first 12):"
PACK=$(ls .git/objects/pack/*.idx)
git verify-pack -v "$PACK" | grep blob | head -12 | sed 's/^/    /'
echo "  (columns: sha1 type size size-in-pack offset [depth base-sha1])"
echo "how many blobs are stored whole vs as deltas:"
git verify-pack -v "$PACK" | grep " blob " | awk '{print (NF>5 ? "delta" : "full-text")}' | sort | uniq -c | sed 's/^/    /'
echo "which revisions are the full-text bases (git gc pack):"
git verify-pack -v "$PACK" | grep " blob " | awk 'NF==5{print $1}' > /tmp/_fulltext.$$
git rev-list --reverse HEAD | cat -n | while read -r n c; do
  B=$(git rev-parse "$c:big.txt")
  if grep -q "$B" /tmp/_fulltext.$$; then echo "    revision $n of 31 -> $B (stored whole)"; fi
done
rm -f /tmp/_fulltext.$$
echo "    newest revision is $(git rev-parse HEAD:big.txt)"

echo
echo "##### E. reachability and gc"
cd "$W"; mkdir g && cd g && git init -q .
printf '1\n' > f; git add .; git commit -qm c1
git checkout -q -b tmp; printf '2\n' > f; git add .; git commit -qm c2
DOOMED=$(git rev-parse HEAD)
git checkout -q master 2>/dev/null || git checkout -q main
git branch -qD tmp
echo "deleted branch tip $DOOMED still readable: $(git cat-file -t $DOOMED)"
echo "fsck says:"; git fsck --unreachable 2>/dev/null | sed 's/^/    /'
echo "reflog still references it:"; git reflog --all | grep -c . | sed 's/^/    reflog entries: /'
git reflog expire --expire=now --all
git gc -q --prune=now
echo "after reflog expire + gc --prune=now:"
git cat-file -t $DOOMED 2>&1 | sed 's/^/    /'

echo
echo "##### F. the index"
cd "$W/r1"
echo "index entries:"; git ls-files --stage | sed 's/^/    /'
echo "index file size: $(wc -c < .git/index) bytes"
T1=$(git write-tree)
rm .git/index
git read-tree HEAD
T2=$(git write-tree)
echo "tree from original index : $T1"
echo "index deleted, rebuilt from commit, tree again: $T2"
echo "-> index reconstructible from the object db for a clean tree."

echo
echo "##### G. object identity is invariant under re-encoding of the pack"
cd "$W/p"
sig() { git cat-file --batch-all-objects --batch-check='%(objectname) %(objecttype) %(objectsize)' | sort | shasum -a 256 | cut -c1-64; }
echo "object-set signature, default deltas : $(sig)"
echo "  pack bytes: $(du -sh .git/objects | cut -f1)"
git repack -a -d -f --depth=1 --window=0 -q
echo "object-set signature, deltas disabled: $(sig)"
echo "  pack bytes: $(du -sh .git/objects | cut -f1)"
git verify-pack -v .git/objects/pack/*.idx | grep " blob " | awk 'NF>5{c++} END{print "  deltified blobs now: " c+0}'
echo "-> the pack encoding is not part of any object's name."

echo
echo "##### H. which revision became the full-text delta base?"
git repack -a -d -q -f
BASE=$(git verify-pack -v .git/objects/pack/*.idx | grep " blob " | awk 'NF==5{print $1, $3}' | sort -k2 -n -r | head -1 | cut -d' ' -f1)
echo "non-delta (full-text) blob in pack: $BASE"
git rev-list --reverse HEAD | cat -n | while read -r n c; do
  B=$(git rev-parse "$c:big.txt")
  if [ "$B" = "$BASE" ]; then
    echo "  it is revision $n of $(git rev-list --count HEAD) ($(git log -1 --format=%s "$c"))"
  fi
done
echo "  oldest revision blob: $(git rev-parse "$(git rev-list --max-parents=0 HEAD):big.txt")"
echo "  newest revision blob: $(git rev-parse HEAD:big.txt)"

echo
echo "WORKDIR=$W"
