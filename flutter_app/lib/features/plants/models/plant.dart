// This file re-exports the new UI-level plant model to avoid duplicate
// `Plant` definitions across layers. Importing `package:cultivar_app/features/plants/models/plant.dart`
// will now provide `PlantUiModel` from `plant_ui_model.dart`.

export 'plant_ui_model.dart';
