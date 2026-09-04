The refusal names one rejected root field: `default_prefix`. Removing it, changing nothing else.

BEGIN_ONTOLOGY_YAML
id: https://malleus.dev/schema/proposals/oceanic-spreading-center
name: oceanic_spreading_center
version: 0.1.0
title: Oceanic Spreading Center Domain Ontology Proposal
description: >-
  Proposed domain vocabulary for accreting oceanic plate boundaries: along-axis
  subsections, the faults and seafloor features that mark them, subsurface
  horizons beneath them, located seismicity, deployed seismic instruments,
  subsurface velocity models, sampled rocks, melt phases, and the chemical
  concentrations, element-ratio proxies, and volatile saturation conditions
  attached to those. Every record class extends a Malleus root primitive, and
  every field declared here is a required scalar with a declared range. This
  document is a proposal. It is not accepted knowledge, and it declares no
  claim, interpretation, decision, or source locator.

default_range: string

prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  osc: https://malleus.dev/schema/proposals/oceanic-spreading-center/

imports:
  - linkml:types
  - malleus

enums:

  GeodynamicRelationType:
    description: >-
      Closed set of predicates asserted between records of this domain. One
      concrete relation class pins exactly one of these values.
    permissible_values:
      HOSTS_SEISMICITY:
        description: The subsection within which a located rupture lies.
      HAS_MAGNITUDE_ESTIMATE:
        description: The rupture a magnitude estimate is reported for.
      SUMMARIZES_SEISMICITY_DEPTH:
        description: The subsection a maximum-depth summary reports on.
      LIES_BENEATH:
        description: The subsection a subsurface horizon lies beneath.
      DESCRIBES_CRUSTAL_STRUCTURE:
        description: The subsection a crustal section describes.
      CUTS:
        description: The subsection whose surface a fault structure cuts.
      BOUNDS:
        description: The subsection a fault structure terminates laterally.
      LOCATED_WITHIN:
        description: The subsection a seafloor feature lies within.
      SAMPLED_FROM:
        description: The subsection a rock sample was recovered from.
      CHARACTERIZES_SAMPLE:
        description: The rock sample a chemical concentration applies to.
      CHARACTERIZES_MELT:
        description: The melt phase a chemical concentration applies to.
      ESTIMATED_FROM_RATIO:
        description: The element-ratio proxy a calculated concentration was derived through.
      SATURATES_AT:
        description: The saturation condition at which a melt phase reaches volatile saturation.
      GENERATED_BENEATH:
        description: The subsection beneath which a melt phase was generated.
      REPRESENTS_MELT:
        description: The melt phase a recovered rock sample stands for.
      DEPLOYED_IN:
        description: The deployment a station was installed as part of.
      LOCATED_WITH_VELOCITY_MODEL:
        description: The velocity model a hypocenter was determined against.
      OFFSETS:
        description: The spreading segment displaced along strike by a discontinuity.

  AccretionMode:
    description: How plate separation is accommodated across an axial subsection.
    permissible_values:
      MAGMATIC:
        description: Separation accommodated mainly by melt supply and volcanic construction.
      AMAGMATIC:
        description: Separation accommodated mainly by faulting and mantle exhumation.
      MIXED:
        description: Separation accommodated by both melt supply and faulting.

  FaultKind:
    description: Structural class of a mapped deformation surface or zone.
    permissible_values:
      NORMAL:
        description: Dip-slip surface accommodating extension.
      DETACHMENT:
        description: Low-angle surface exhuming footwall rocks.
      TRANSFORM:
        description: Strike-slip plate boundary offsetting accreting subsections.
      SHEAR_ZONE:
        description: Distributed ductile to semi-brittle deformation zone.

  StructureActivityState:
    description: Whether a structure or feature is presently active.
    permissible_values:
      ACTIVE:
        description: Presently accumulating deformation, venting, or eruption.
      INACTIVE:
        description: Preserved but no longer accumulating deformation, venting, or eruption.

  SeafloorFeatureKind:
    description: Morphologic or volcanic expression mapped at the seafloor.
    permissible_values:
      AXIAL_VALLEY:
        description: Fault-bounded depression along an accreting axis.
      NEOVOLCANIC_RIDGE:
        description: Youngest volcanic construction along an accreting axis.
      VOLCANIC_CONE:
        description: Discrete constructional volcanic edifice.
      HUMMOCKY_TERRAIN:
        description: Rough terrain built by coalesced volcanic mounds.
      CORRUGATED_SURFACE:
        description: Striated exposed fault surface.
      OCEANIC_CORE_COMPLEX:
        description: Domed exposure of footwall rocks unroofed by a detachment.
      HYDROTHERMAL_FIELD:
        description: Area of focused hydrothermal discharge or its deposits.
      TRANSVERSE_RIDGE:
        description: Elevated ridge flanking a transform valley.
      SUSPENDED_VALLEY:
        description: Valley segment perched above an adjoining transform valley floor.
      FRACTURE_ZONE:
        description: Inactive trace of a transform boundary on older lithosphere.
      SEAMOUNT:
        description: Isolated submarine volcanic edifice off an axis.

  LithosphericInterfaceKind:
    description: Mechanical or compositional interface within the lithosphere.
    permissible_values:
      BRITTLE_DUCTILE_BOUNDARY:
        description: Depth below which deformation ceases to nucleate brittle rupture.
      CRUST_MANTLE_BOUNDARY:
        description: Compositional interface between crust and underlying mantle.
      LITHOSPHERE_ASTHENOSPHERE_BOUNDARY:
        description: Base of the mechanically coherent plate.

  DepthDatum:
    description: Reference surface from which a depth is measured downward.
    permissible_values:
      BELOW_SEAFLOOR:
        description: Measured downward from the seafloor.
      BELOW_SEA_LEVEL:
        description: Measured downward from mean sea level.

  MagnitudeScale:
    description: Scale a reported earthquake magnitude was computed on.
    permissible_values:
      LOCAL:
        description: Amplitude-based local magnitude scale.
      MOMENT:
        description: Seismic-moment-based magnitude scale.

  Lithology:
    description: Rock class of a recovered sample.
    permissible_values:
      BASALT:
        description: Erupted mafic volcanic rock.
      PERIDOTITE:
        description: Ultramafic mantle rock.
      MYLONITE:
        description: Rock fabric produced by ductile shear.

  SampleMaterialForm:
    description: Physical form of the material a concentration was determined on.
    permissible_values:
      WHOLE_ROCK:
        description: Bulk rock aliquot.
      VOLCANIC_GLASS:
        description: Quenched melt glass.
      MELT_INCLUSION:
        description: Melt trapped within a host crystal.

  AnalyteKind:
    description: Geochemical role of the analyte a concentration reports.
    permissible_values:
      MAJOR_ELEMENT:
        description: Element present at major abundance in the rock or melt.
      TRACE_ELEMENT:
        description: Element present at trace abundance.
      VOLATILE_COMPONENT:
        description: Component that partitions into a fluid or gas phase on decompression.

  ConcentrationUnit:
    description: Unit a concentration value is expressed in.
    permissible_values:
      WEIGHT_PERCENT:
        description: Mass fraction expressed as percent.
      PARTS_PER_MILLION:
        description: Mass fraction expressed as parts per million.

  DeterminationMode:
    description: How a concentration value was obtained.
    permissible_values:
      MEASURED:
        description: Determined by analysis of the material itself.
      CALCULATED:
        description: Derived from other quantities through a declared relationship.

  MeltStage:
    description: Stage of melt evolution a record refers to.
    permissible_values:
      PRIMARY:
        description: Melt in equilibrium with its mantle source.
      PRE_ERUPTIVE:
        description: Melt after crystallization but before eruption and volatile loss.
      ERUPTED:
        description: Melt emplaced at the seafloor.

  VelocityModelDimensionality:
    description: Spatial dimensionality of a seismic velocity model.
    permissible_values:
      ONE_DIMENSIONAL:
        description: Velocity varies with depth only.
      THREE_DIMENSIONAL:
        description: Velocity varies in all three spatial directions.

  StationDataState:
    description: Whether a deployed station yielded usable records.
    permissible_values:
      DATA_RECOVERED:
        description: Station returned usable continuous records.
      NO_DATA_RECOVERED:
        description: Station returned no usable records.

slots:

  axial_length:
    range: float
    required: true
    minimum_value: 0.0
    description: Along-axis extent of the subsection, in kilometers.

  trend_azimuth:
    range: float
    required: true
    minimum_value: 0.0
    maximum_value: 360.0
    description: Azimuth of the subsection trend, in degrees clockwise from north.

  full_spreading_rate:
    range: float
    required: true
    minimum_value: 0.0
    description: Total separation rate across the plate boundary, in millimeters per year.

  accretion_mode:
    range: AccretionMode
    required: true
    description: How plate separation is accommodated across the subsection.

  axial_offset:
    range: float
    required: true
    minimum_value: 0.0
    description: Along-strike displacement of the axis across the discontinuity, in kilometers.

  fault_kind:
    range: FaultKind
    required: true
    description: Structural class of the deformation surface or zone.

  strike_azimuth:
    range: float
    required: true
    minimum_value: 0.0
    maximum_value: 360.0
    description: Azimuth of the structure strike, in degrees clockwise from north.

  activity_state:
    range: StructureActivityState
    required: true
    description: Whether the structure or feature is presently active.

  feature_kind:
    range: SeafloorFeatureKind
    required: true
    description: Morphologic or volcanic expression the feature belongs to.

  horizon_depth:
    range: float
    required: true
    minimum_value: 0.0
    description: Depth of the horizon below its declared datum, in kilometers.

  depth_datum:
    range: DepthDatum
    required: true
    description: Reference surface the depth is measured from.

  interface_kind:
    range: LithosphericInterfaceKind
    required: true
    description: Mechanical or compositional interface the horizon represents.

  temperature:
    range: float
    required: true
    description: Temperature of the represented condition, in degrees Celsius.

  pressure:
    range: float
    required: true
    minimum_value: 0.0
    description: Pressure of the represented condition, in gigapascals.

  crustal_thickness:
    range: float
    required: true
    minimum_value: 0.0
    description: Thickness of the crustal column, in kilometers.

  thickness_uncertainty:
    range: float
    required: true
    minimum_value: 0.0
    description: Reported uncertainty on the thickness, in kilometers.

  crustal_age:
    range: float
    required: true
    minimum_value: 0.0
    description: Age of the crust in the column, in millions of years.

  latitude:
    range: float
    required: true
    minimum_value: -90.0
    maximum_value: 90.0
    description: Latitude of the record position, in decimal degrees north.

  longitude:
    range: float
    required: true
    minimum_value: -180.0
    maximum_value: 180.0
    description: Longitude of the record position, in decimal degrees east.

  hypocentral_depth:
    range: float
    required: true
    minimum_value: 0.0
    description: Depth of the rupture hypocenter below its declared datum, in kilometers.

  depth_uncertainty:
    range: float
    required: true
    minimum_value: 0.0
    description: Reported uncertainty on the hypocentral depth, in kilometers.

  epicentral_uncertainty:
    range: float
    required: true
    minimum_value: 0.0
    description: Reported horizontal uncertainty on the epicenter, in kilometers.

  azimuthal_station_gap:
    range: float
    required: true
    minimum_value: 0.0
    maximum_value: 360.0
    description: Largest azimuthal gap between recording stations, in degrees.

  travel_time_residual:
    range: float
    required: true
    minimum_value: 0.0
    description: Root-mean-square arrival-time residual of the location, in seconds.

  satisfied_criteria_count:
    range: integer
    required: true
    minimum_value: 0
    description: Number of the declared location-quality criteria the solution satisfies.

  maximum_hypocentral_depth:
    range: float
    required: true
    minimum_value: 0.0
    description: Deepest hypocentral depth summarized for the subsection, in kilometers.

  supporting_event_count:
    range: integer
    required: true
    minimum_value: 1
    description: Number of ruptures the summarized maximum depth rests on.

  magnitude_scale:
    range: MagnitudeScale
    required: true
    description: Scale the magnitude value was computed on.

  magnitude_value:
    range: float
    required: true
    description: Magnitude value on the declared scale.

  station_count:
    range: integer
    required: true
    minimum_value: 1
    description: Number of stations installed in the deployment.

  mean_station_spacing:
    range: float
    required: true
    minimum_value: 0.0
    description: Mean separation between neighboring stations, in kilometers.

  recording_duration:
    range: float
    required: true
    minimum_value: 0.0
    description: Length of continuous recording, in days.

  station_data_state:
    range: StationDataState
    required: true
    description: Whether the station yielded usable records.

  model_dimensionality:
    range: VelocityModelDimensionality
    required: true
    description: Spatial dimensionality of the velocity model.

  p_to_s_velocity_ratio:
    range: float
    required: true
    minimum_value: 0.0
    description: Ratio of compressional to shear wave speed assumed by the model.

  maximum_constrained_depth:
    range: float
    required: true
    minimum_value: 0.0
    description: Greatest depth at which the model is constrained by data, in kilometers.

  lithology:
    range: Lithology
    required: true
    description: Rock class of the recovered sample.

  material_form:
    range: SampleMaterialForm
    required: true
    description: Physical form of the analyzed material.

  sampling_water_depth:
    range: float
    required: true
    minimum_value: 0.0
    description: Water depth at which the sample was recovered, in meters.

  analyte_symbol:
    range: string
    required: true
    description: >-
      Symbol of the element or oxide component the record refers to, as written
      by the reporting analysis.

  analyte_kind:
    range: AnalyteKind
    required: true
    description: Geochemical role of the analyte.

  concentration_value:
    range: float
    required: true
    minimum_value: 0.0
    description: Concentration of the analyte in the declared unit.

  concentration_unit:
    range: ConcentrationUnit
    required: true
    description: Unit the concentration value is expressed in.

  determination_mode:
    range: DeterminationMode
    required: true
    description: Whether the concentration was measured or calculated.

  melt_stage:
    range: MeltStage
    required: true
    description: Stage of melt evolution the record refers to.

  numerator_symbol:
    range: string
    required: true
    description: Symbol of the component in the numerator of the ratio.

  denominator_symbol:
    range: string
    required: true
    description: Symbol of the component in the denominator of the ratio.

  ratio_value:
    range: float
    required: true
    minimum_value: 0.0
    description: Value of the concentration ratio between the two named components.

  ratio_uncertainty:
    range: float
    required: true
    minimum_value: 0.0
    description: Reported uncertainty on the ratio value.

classes:

  RidgeAxisSubsection:
    is_a: Entity
    abstract: true
    description: >-
      A length of accreting plate boundary treated as one along-axis unit,
      carrying the geometry and spreading properties shared by accreting
      segments and the discontinuities that separate them.
    slots:
      - axial_length
      - trend_azimuth
      - full_spreading_rate
      - accretion_mode

  SpreadingSegment:
    is_a: RidgeAxisSubsection
    description: >-
      An accreting subsection between two discontinuities, where new crust is
      emplaced along the axis. Declared as its own class so that relations about
      melt generation, crustal structure, and along-strike offset can pin an
      accreting segment rather than any subsection.

  SegmentDiscontinuity:
    is_a: RidgeAxisSubsection
    description: >-
      A subsection that displaces the axis along strike without a transform
      fault, separating two accreting segments.
    slots:
      - axial_offset

  SubsurfaceHorizon:
    is_a: Entity
    abstract: true
    description: >-
      A surface at depth beneath an axial subsection, located by one depth below
      a declared datum.
    slots:
      - horizon_depth
      - depth_datum

  LithosphericInterface:
    is_a: SubsurfaceHorizon
    description: A mechanical or compositional interface within the lithosphere.
    slots:
      - interface_kind

  IsothermSurface:
    is_a: SubsurfaceHorizon
    description: A surface of constant temperature at depth.
    slots:
      - temperature

  CrustalSection:
    is_a: Entity
    description: >-
      A dated crustal column of declared thickness beneath one place on or off
      the axis.
    slots:
      - crustal_thickness
      - thickness_uncertainty
      - crustal_age

  FaultStructure:
    is_a: Entity
    description: A mapped deformation surface or zone of declared class and strike.
    slots:
      - fault_kind
      - strike_azimuth
      - activity_state

  SeafloorFeature:
    is_a: Entity
    description: A mapped morphologic or volcanic expression at the seafloor.
    slots:
      - feature_kind
      - activity_state

  Earthquake:
    is_a: Entity
    description: >-
      One located rupture, carrying its hypocenter, the uncertainties reported
      with it, and the constraints that its location solution satisfies.
    slots:
      - latitude
      - longitude
      - hypocentral_depth
      - depth_datum
      - depth_uncertainty
      - epicentral_uncertainty
      - azimuthal_station_gap
      - travel_time_residual
      - satisfied_criteria_count

  MagnitudeEstimate:
    is_a: Entity
    description: One magnitude value reported for one rupture on a declared scale.
    slots:
      - magnitude_scale
      - magnitude_value

  SeismicityDepthSummary:
    is_a: Entity
    description: >-
      The deepest hypocentral depth attributed to one axial subsection and the
      number of ruptures that depth rests on.
    slots:
      - maximum_hypocentral_depth
      - depth_datum
      - supporting_event_count

  SeismicStation:
    is_a: Entity
    description: One installed recording station at a declared position.
    slots:
      - latitude
      - longitude
      - station_data_state

  SeismicDeployment:
    is_a: Entity
    description: >-
      One installation of a station network, carrying its size, geometry, and
      recording span.
    slots:
      - station_count
      - mean_station_spacing
      - recording_duration

  SeismicVelocityModel:
    is_a: Entity
    description: >-
      A model of subsurface wave speed used to convert arrival times into
      positions.
    slots:
      - model_dimensionality
      - p_to_s_velocity_ratio
      - maximum_constrained_depth

  RockSample:
    is_a: Entity
    description: One recovered rock or glass sample at a declared position.
    slots:
      - lithology
      - material_form
      - latitude
      - longitude
      - sampling_water_depth

  ChemicalConcentration:
    is_a: Entity
    description: >-
      The concentration of one analyte in one material or melt phase, in a
      declared unit, either measured or calculated.
    slots:
      - analyte_symbol
      - analyte_kind
      - concentration_value
      - concentration_unit
      - determination_mode

  MeltPhase:
    is_a: Entity
    description: Melt at one declared stage of its evolution from source to seafloor.
    slots:
      - melt_stage

  VolatileSaturationCondition:
    is_a: Entity
    description: >-
      The pressure and temperature at which a melt reaches saturation in one
      volatile component and begins to exsolve it.
    slots:
      - analyte_symbol
      - pressure
      - temperature

  ElementRatioProxy:
    is_a: Entity
    description: >-
      A concentration ratio between two components, with its uncertainty, used
      to derive one component from the other.
    slots:
      - numerator_symbol
      - denominator_symbol
      - ratio_value
      - ratio_uncertainty

  HostsSeismicityRelation:
    is_a: Relation
    description: An axial subsection contains a located rupture.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: HOSTS_SEISMICITY
      source_id:
        range: RidgeAxisSubsection
        required: true
      target_id:
        range: Earthquake
        required: true

  HasMagnitudeEstimateRelation:
    is_a: Relation
    description: A rupture is reported with a magnitude estimate.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: HAS_MAGNITUDE_ESTIMATE
      source_id:
        range: Earthquake
        required: true
      target_id:
        range: MagnitudeEstimate
        required: true

  SummarizesSeismicityDepthRelation:
    is_a: Relation
    description: A maximum-depth summary reports on an axial subsection.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: SUMMARIZES_SEISMICITY_DEPTH
      source_id:
        range: SeismicityDepthSummary
        required: true
      target_id:
        range: RidgeAxisSubsection
        required: true

  LiesBeneathRelation:
    is_a: Relation
    description: A subsurface horizon lies beneath an axial subsection.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: LIES_BENEATH
      source_id:
        range: SubsurfaceHorizon
        required: true
      target_id:
        range: RidgeAxisSubsection
        required: true

  DescribesCrustalStructureRelation:
    is_a: Relation
    description: A crustal column describes the crust of an axial subsection.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: DESCRIBES_CRUSTAL_STRUCTURE
      source_id:
        range: CrustalSection
        required: true
      target_id:
        range: RidgeAxisSubsection
        required: true

  CutsSubsectionRelation:
    is_a: Relation
    description: A fault structure cuts the surface of an axial subsection.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: CUTS
      source_id:
        range: FaultStructure
        required: true
      target_id:
        range: RidgeAxisSubsection
        required: true

  BoundsSubsectionRelation:
    is_a: Relation
    description: A fault structure terminates an axial subsection laterally.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: BOUNDS
      source_id:
        range: FaultStructure
        required: true
      target_id:
        range: RidgeAxisSubsection
        required: true

  FeatureLocatedWithinRelation:
    is_a: Relation
    description: A seafloor feature lies within an axial subsection.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: LOCATED_WITHIN
      source_id:
        range: SeafloorFeature
        required: true
      target_id:
        range: RidgeAxisSubsection
        required: true

  SampledFromRelation:
    is_a: Relation
    description: A rock sample was recovered from an axial subsection.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: SAMPLED_FROM
      source_id:
        range: RockSample
        required: true
      target_id:
        range: RidgeAxisSubsection
        required: true

  CharacterizesSampleRelation:
    is_a: Relation
    description: A chemical concentration applies to a rock sample.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: CHARACTERIZES_SAMPLE
      source_id:
        range: ChemicalConcentration
        required: true
      target_id:
        range: RockSample
        required: true

  CharacterizesMeltRelation:
    is_a: Relation
    description: A chemical concentration applies to a melt phase.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: CHARACTERIZES_MELT
      source_id:
        range: ChemicalConcentration
        required: true
      target_id:
        range: MeltPhase
        required: true

  EstimatedFromRatioRelation:
    is_a: Relation
    description: A calculated concentration was derived through an element-ratio proxy.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: ESTIMATED_FROM_RATIO
      source_id:
        range: ChemicalConcentration
        required: true
      target_id:
        range: ElementRatioProxy
        required: true

  SaturatesAtRelation:
    is_a: Relation
    description: A melt phase reaches volatile saturation at a saturation condition.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: SATURATES_AT
      source_id:
        range: MeltPhase
        required: true
      target_id:
        range: VolatileSaturationCondition
        required: true

  GeneratedBeneathRelation:
    is_a: Relation
    description: A melt phase was generated beneath an accreting segment.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: GENERATED_BENEATH
      source_id:
        range: MeltPhase
        required: true
      target_id:
        range: SpreadingSegment
        required: true

  RepresentsMeltRelation:
    is_a: Relation
    description: A recovered rock sample stands for a melt phase.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: REPRESENTS_MELT
      source_id:
        range: RockSample
        required: true
      target_id:
        range: MeltPhase
        required: true

  DeployedInRelation:
    is_a: Relation
    description: A station was installed as part of a deployment.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: DEPLOYED_IN
      source_id:
        range: SeismicStation
        required: true
      target_id:
        range: SeismicDeployment
        required: true

  LocatedWithVelocityModelRelation:
    is_a: Relation
    description: A hypocenter was determined against a seismic velocity model.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: LOCATED_WITH_VELOCITY_MODEL
      source_id:
        range: Earthquake
        required: true
      target_id:
        range: SeismicVelocityModel
        required: true

  OffsetsSegmentRelation:
    is_a: Relation
    description: A discontinuity displaces an accreting segment along strike.
    slot_usage:
      relation_type:
        range: GeodynamicRelationType
        required: true
        equals_string: OFFSETS
      source_id:
        range: SegmentDiscontinuity
        required: true
      target_id:
        range: SpreadingSegment
        required: true
END_ONTOLOGY_YAML