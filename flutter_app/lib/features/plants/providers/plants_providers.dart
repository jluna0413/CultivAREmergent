import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/providers/api_client_provider.dart';
import '../data/plants_api_client.dart';
import '../domain/plant_model.dart';

final plantsApiClientProvider = Provider<PlantsApiClient>((ref) {
  return PlantsApiClient(ref.read(apiClientProvider));
});

// List plants with pagination and filtering support
final plantsListProvider = FutureProvider.autoDispose
    .family<PaginatedPlantsResponse, PlantsParams>((ref, params) {
      return ref
          .watch(plantsApiClientProvider)
          .getPlants(
            page: params.page,
            limit: params.limit,
            status: params.status,
            search: params.search,
            cultivarId: params.cultivarId,
            zoneId: params.zoneId,
            sortBy: params.sortBy,
            sortOrder: params.sortOrder,
          );
    });

// Get individual plant by ID
final plantProvider = FutureProvider.family<Plant, int>((ref, id) {
  return ref.watch(plantsApiClientProvider).getPlant(id);
});

// Create plant - using simple provider approach
final createPlantProvider = FutureProvider.family<Plant, PlantCreate>((
  ref,
  plantData,
) async {
  final apiClient = ref.read(plantsApiClientProvider);
  final newPlant = await apiClient.createPlant(plantData);
  // Invalidate plants list to refresh the UI
  ref.invalidate(plantsListProvider);
  return newPlant;
});

// Update plant - using simple provider approach
final updatePlantProvider = FutureProvider.family<Plant, UpdatePlantRequest>((
  ref,
  request,
) async {
  final apiClient = ref.read(plantsApiClientProvider);
  final updatedPlant = await apiClient.updatePlant(request.id, request.data);
  // Invalidate related providers to refresh the UI
  ref.invalidate(plantsListProvider);
  ref.invalidate(plantProvider(request.id));
  return updatedPlant;
});

// Delete plant - using simple provider approach
final deletePlantProvider = FutureProvider.family<void, int>((
  ref,
  plantId,
) async {
  final apiClient = ref.read(plantsApiClientProvider);
  await apiClient.deletePlant(plantId);
  // Invalidate related providers to refresh the UI
  ref.invalidate(plantsListProvider);
  ref.invalidate(plantProvider(plantId));
});

// Helper classes for request parameters
class UpdatePlantRequest {
  const UpdatePlantRequest(this.id, this.data);
  final int id;
  final PlantUpdate data;
}

// AsyncValue convenience providers for plants list
final plantsListLoadingProvider = Provider.autoDispose
    .family<bool, PlantsParams>((ref, params) {
      final asyncValue = ref.watch(plantsListProvider(params));
      return asyncValue.isLoading;
    });

final plantsListErrorProvider = Provider.autoDispose
    .family<String?, PlantsParams>((ref, params) {
      final asyncValue = ref.watch(plantsListProvider(params));
      return asyncValue.maybeWhen(
        error: (error, _) => error.toString(),
        orElse: () => null,
      );
    });

final plantsListDataProvider = Provider.autoDispose
    .family<PaginatedPlantsResponse?, PlantsParams>((ref, params) {
      final asyncValue = ref.watch(plantsListProvider(params));
      return asyncValue.maybeWhen(data: (data) => data, orElse: () => null);
    });

// AsyncValue convenience providers for plant detail
final plantDetailLoadingProvider = Provider.family<bool, int>((ref, id) {
  final asyncValue = ref.watch(plantProvider(id));
  return asyncValue.isLoading;
});

final plantDetailErrorProvider = Provider.family<String?, int>((ref, id) {
  final asyncValue = ref.watch(plantProvider(id));
  return asyncValue.maybeWhen(
    error: (error, _) => error.toString(),
    orElse: () => null,
  );
});

final plantDetailDataProvider = Provider.family<Plant?, int>((ref, id) {
  final asyncValue = ref.watch(plantProvider(id));
  return asyncValue.maybeWhen(data: (data) => data, orElse: () => null);
});

// AsyncValue convenience providers for create plant
final createPlantLoadingProvider = Provider.family<bool, PlantCreate>((
  ref,
  data,
) {
  final asyncValue = ref.watch(createPlantProvider(data));
  return asyncValue.isLoading;
});

final createPlantErrorProvider = Provider.family<String?, PlantCreate>((
  ref,
  data,
) {
  final asyncValue = ref.watch(createPlantProvider(data));
  return asyncValue.maybeWhen(
    error: (error, _) => error.toString(),
    orElse: () => null,
  );
});

final createPlantSuccessProvider = Provider.family<Plant?, PlantCreate>((
  ref,
  data,
) {
  final asyncValue = ref.watch(createPlantProvider(data));
  return asyncValue.maybeWhen(data: (data) => data, orElse: () => null);
});

// AsyncValue convenience providers for update plant
final updatePlantLoadingProvider = Provider.family<bool, UpdatePlantRequest>((
  ref,
  request,
) {
  final asyncValue = ref.watch(updatePlantProvider(request));
  return asyncValue.isLoading;
});

final updatePlantErrorProvider = Provider.family<String?, UpdatePlantRequest>((
  ref,
  request,
) {
  final asyncValue = ref.watch(updatePlantProvider(request));
  return asyncValue.maybeWhen(
    error: (error, _) => error.toString(),
    orElse: () => null,
  );
});

final updatePlantSuccessProvider = Provider.family<Plant?, UpdatePlantRequest>((
  ref,
  request,
) {
  final asyncValue = ref.watch(updatePlantProvider(request));
  return asyncValue.maybeWhen(data: (data) => data, orElse: () => null);
});

// AsyncValue convenience providers for delete plant
final deletePlantLoadingProvider = Provider.family<bool, int>((ref, plantId) {
  final asyncValue = ref.watch(deletePlantProvider(plantId));
  return asyncValue.isLoading;
});

final deletePlantErrorProvider = Provider.family<String?, int>((ref, plantId) {
  final asyncValue = ref.watch(deletePlantProvider(plantId));
  return asyncValue.maybeWhen(
    error: (error, _) => error.toString(),
    orElse: () => null,
  );
});

final deletePlantSuccessProvider = Provider.family<bool, int>((ref, plantId) {
  final asyncValue = ref.watch(deletePlantProvider(plantId));
  return asyncValue.maybeWhen(data: (_) => true, orElse: () => false);
});
