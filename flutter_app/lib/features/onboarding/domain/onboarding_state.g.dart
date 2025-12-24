// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'onboarding_state.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$GeneticItemImpl _$$GeneticItemImplFromJson(Map<String, dynamic> json) =>
    _$GeneticItemImpl(
      id: json['id'] as String,
      strainName: json['strainName'] as String,
      breederName: json['breederName'] as String,
      type: $enumDecode(_$GeneticTypeEnumMap, json['type']),
      packagingImageUrl: json['packagingImageUrl'] as String?,
    );

Map<String, dynamic> _$$GeneticItemImplToJson(_$GeneticItemImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'strainName': instance.strainName,
      'breederName': instance.breederName,
      'type': _$GeneticTypeEnumMap[instance.type]!,
      'packagingImageUrl': instance.packagingImageUrl,
    };

const _$GeneticTypeEnumMap = {
  GeneticType.seed: 'seed',
  GeneticType.clone: 'clone',
};

_$PotPositionDataImpl _$$PotPositionDataImplFromJson(
  Map<String, dynamic> json,
) => _$PotPositionDataImpl(
  id: json['id'] as String,
  potSizeLabel: json['potSizeLabel'] as String,
  potType: json['potType'] as String? ?? 'fabric',
  xPosition: (json['xPosition'] as num).toDouble(),
  yPosition: (json['yPosition'] as num).toDouble(),
);

Map<String, dynamic> _$$PotPositionDataImplToJson(
  _$PotPositionDataImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'potSizeLabel': instance.potSizeLabel,
  'potType': instance.potType,
  'xPosition': instance.xPosition,
  'yPosition': instance.yPosition,
};

_$EnvironmentConfigImpl _$$EnvironmentConfigImplFromJson(
  Map<String, dynamic> json,
) => _$EnvironmentConfigImpl(
  name: json['name'] as String,
  environmentType: $enumDecode(
    _$EnvironmentTypeEnumMap,
    json['environmentType'],
  ),
  tentWidthInches: (json['tentWidthInches'] as num?)?.toDouble(),
  tentDepthInches: (json['tentDepthInches'] as num?)?.toDouble(),
  tentSizeLabel: json['tentSizeLabel'] as String?,
  pots:
      (json['pots'] as List<dynamic>?)
          ?.map((e) => PotPositionData.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
);

Map<String, dynamic> _$$EnvironmentConfigImplToJson(
  _$EnvironmentConfigImpl instance,
) => <String, dynamic>{
  'name': instance.name,
  'environmentType': _$EnvironmentTypeEnumMap[instance.environmentType]!,
  'tentWidthInches': instance.tentWidthInches,
  'tentDepthInches': instance.tentDepthInches,
  'tentSizeLabel': instance.tentSizeLabel,
  'pots': instance.pots,
};

const _$EnvironmentTypeEnumMap = {
  EnvironmentType.tent: 'tent',
  EnvironmentType.greenhouse: 'greenhouse',
  EnvironmentType.outdoors: 'outdoors',
};

_$HardwareIntegrationImpl _$$HardwareIntegrationImplFromJson(
  Map<String, dynamic> json,
) => _$HardwareIntegrationImpl(
  manufacturer: $enumDecode(
    _$HardwareManufacturerEnumMap,
    json['manufacturer'],
  ),
  isLinked: json['isLinked'] as bool? ?? false,
  linkedAccountId: json['linkedAccountId'] as String?,
);

Map<String, dynamic> _$$HardwareIntegrationImplToJson(
  _$HardwareIntegrationImpl instance,
) => <String, dynamic>{
  'manufacturer': _$HardwareManufacturerEnumMap[instance.manufacturer]!,
  'isLinked': instance.isLinked,
  'linkedAccountId': instance.linkedAccountId,
};

const _$HardwareManufacturerEnumMap = {
  HardwareManufacturer.acInfinity: 'acInfinity',
  HardwareManufacturer.ecowitt: 'ecowitt',
  HardwareManufacturer.vivosun: 'vivosun',
  HardwareManufacturer.spiderFarmer: 'spiderFarmer',
  HardwareManufacturer.marsHydro: 'marsHydro',
  HardwareManufacturer.other: 'other',
};

_$OnboardingStateImpl _$$OnboardingStateImplFromJson(
  Map<String, dynamic> json,
) => _$OnboardingStateImpl(
  currentStep:
      $enumDecodeNullable(_$OnboardingStepEnumMap, json['currentStep']) ??
      OnboardingStep.welcome,
  genetics:
      (json['genetics'] as List<dynamic>?)
          ?.map((e) => GeneticItem.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  environmentConfig: json['environmentConfig'] == null
      ? null
      : EnvironmentConfig.fromJson(
          json['environmentConfig'] as Map<String, dynamic>,
        ),
  integrations:
      (json['integrations'] as List<dynamic>?)
          ?.map((e) => HardwareIntegration.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  isCompleted: json['isCompleted'] as bool? ?? false,
  isSubmitting: json['isSubmitting'] as bool? ?? false,
  error: json['error'] as String?,
  selectedEnvironmentType: $enumDecodeNullable(
    _$EnvironmentTypeEnumMap,
    json['selectedEnvironmentType'],
  ),
  selectedTentSize: json['selectedTentSize'] as String?,
  selectedPotSize: json['selectedPotSize'] as String?,
);

Map<String, dynamic> _$$OnboardingStateImplToJson(
  _$OnboardingStateImpl instance,
) => <String, dynamic>{
  'currentStep': _$OnboardingStepEnumMap[instance.currentStep]!,
  'genetics': instance.genetics,
  'environmentConfig': instance.environmentConfig,
  'integrations': instance.integrations,
  'isCompleted': instance.isCompleted,
  'isSubmitting': instance.isSubmitting,
  'error': instance.error,
  'selectedEnvironmentType':
      _$EnvironmentTypeEnumMap[instance.selectedEnvironmentType],
  'selectedTentSize': instance.selectedTentSize,
  'selectedPotSize': instance.selectedPotSize,
};

const _$OnboardingStepEnumMap = {
  OnboardingStep.welcome: 'welcome',
  OnboardingStep.genetics: 'genetics',
  OnboardingStep.environment: 'environment',
  OnboardingStep.hardware: 'hardware',
  OnboardingStep.complete: 'complete',
};
