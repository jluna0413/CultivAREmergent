import 'package:cultivar_app/core/providers/api_client_provider.dart';
import 'package:cultivar_app/features/plants/data/plants_api_client.dart';
import 'package:cultivar_app/features/plants/domain/plant_model.dart';
import 'package:cultivar_app/features/plants/providers/plants_providers.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dio/dio.dart'; // Import Dio
import 'package:cultivar_app/core/models/plant_models.dart' as i6;
import 'package:cultivar_app/core/models/cultivar_models.dart' as i7;
import 'package:cultivar_app/core/models/sensor_models.dart' as i8;
import 'package:cultivar_app/core/models/cart_models.dart' as i9;
import 'package:cultivar_app/core/models/product_models.dart' as i10;
import 'package:cultivar_app/core/models/auth_models.dart' as i11;
import 'dart:math' as i12;

// Mock classes
class MockPlantsApiClient extends Mock implements PlantsApiClient {}

class MockApiClient extends Mock implements ApiClient {
  @override
  Dio get dio =>
      (super.noSuchMethod(Invocation.getter(#dio), returnValue: Dio()) as Dio);
  @override
  Future<T> get<T>(
    String? path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onReceiveProgress,
  }) =>
      (super.noSuchMethod(
            Invocation.method(
              #get,
              [path],
              {
                #queryParameters: queryParameters,
                #options: options,
                #cancelToken: cancelToken,
                #onReceiveProgress: onReceiveProgress,
              },
            ),
            returnValue: Future.value(null),
          )
          as Future<T>);
  @override
  Future<T> post<T>(
    String? path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) =>
      (super.noSuchMethod(
            Invocation.method(
              #post,
              [path],
              {
                #data: data,
                #queryParameters: queryParameters,
                #options: options,
                #cancelToken: cancelToken,
                #onSendProgress: onSendProgress,
                #onReceiveProgress: onReceiveProgress,
              },
            ),
            returnValue: Future.value(null),
          )
          as Future<T>);
  @override
  Future<T> put<T>(
    String? path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) =>
      (super.noSuchMethod(
            Invocation.method(
              #put,
              [path],
              {
                #data: data,
                #queryParameters: queryParameters,
                #options: options,
                #cancelToken: cancelToken,
                #onSendProgress: onSendProgress,
                #onReceiveProgress: onReceiveProgress,
              },
            ),
            returnValue: Future.value(null),
          )
          as Future<T>);
  @override
  Future<T> delete<T>(
    String? path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
  }) =>
      (super.noSuchMethod(
            Invocation.method(
              #delete,
              [path],
              {
                #data: data,
                #queryParameters: queryParameters,
                #options: options,
                #cancelToken: cancelToken,
              },
            ),
            returnValue: Future.value(null),
          )
          as Future<T>);
  @override
  Future<List<PlantModel>> getPlants() =>
      (super.noSuchMethod(
            Invocation.method(#getPlants, []),
            returnValue: Future<List<PlantModel>>.value(<PlantModel>[]),
          )
          as Future<List<PlantModel>>);
  @override
  Future<List<Cultivar>> getCultivars() =>
      (super.noSuchMethod(
            Invocation.method(#getCultivars, []),
            returnValue: Future<List<Cultivar>>.value(<Cultivar>[]),
          )
          as Future<List<Cultivar>>);
  @override
  Future<List<Sensor>> getAllSensors() =>
      (super.noSuchMethod(
            Invocation.method(#getAllSensors, []),
            returnValue: Future<List<Sensor>>.value(<Sensor>[]),
          )
          as Future<List<Sensor>>);
  @override
  Future<List<CartItem>> getCartItems() =>
      (super.noSuchMethod(
            Invocation.method(#getCartItems, []),
            returnValue: Future<List<CartItem>>.value(<CartItem>[]),
          )
          as Future<List<CartItem>>);
  @override
  Future<List<Product>> getProducts() =>
      (super.noSuchMethod(
            Invocation.method(#getProducts, []),
            returnValue: Future<List<Product>>.value(<Product>[]),
          )
          as Future<List<Product>>);
  @override
  Future<Map<String, dynamic>> getProductsPaginated({
    int? page,
    int? pageSize,
  }) =>
      (super.noSuchMethod(
            Invocation.method(#getProductsPaginated, [], {
              #page: page,
              #pageSize: pageSize,
            }),
            returnValue: Future<Map<String, dynamic>>.value(
              <String, dynamic>{},
            ),
          )
          as Future<Map<String, dynamic>>);
  @override
  Future<Cultivar> getCultivar(int? id) =>
      (super.noSuchMethod(
            Invocation.method(#getCultivar, [id]),
            returnValue: Future<Cultivar>.value(
              Cultivar(
                id: 1,
                name: '',
                description: '',
                genetics: '',
                thcContent: 0,
                cbdContent: 0,
                breederId: 0,
                isActive: true,
                createdAt: DateTime.now(),
                updatedAt: DateTime.now(),
              ),
            ),
          )
          as Future<Cultivar>);
  @override
  Future<Cultivar> createCultivar(dynamic cultivarData) =>
      (super.noSuchMethod(
            Invocation.method(#createCultivar, [cultivarData]),
            returnValue: Future<Cultivar>.value(
              Cultivar(
                id: 1,
                name: '',
                description: '',
                genetics: '',
                thcContent: 0,
                cbdContent: 0,
                breederId: 0,
                isActive: true,
                createdAt: DateTime.now(),
                updatedAt: DateTime.now(),
              ),
            ),
          )
          as Future<Cultivar>);
  @override
  Future<Cultivar> updateCultivar(int? id, dynamic cultivarData) =>
      (super.noSuchMethod(
            Invocation.method(#updateCultivar, [id, cultivarData]),
            returnValue: Future<Cultivar>.value(
              Cultivar(
                id: 1,
                name: '',
                description: '',
                genetics: '',
                thcContent: 0,
                cbdContent: 0,
                breederId: 0,
                isActive: true,
                createdAt: DateTime.now(),
                updatedAt: DateTime.now(),
              ),
            ),
          )
          as Future<Cultivar>);
  @override
  Future<void> deleteCultivar(int? id) =>
      (super.noSuchMethod(
            Invocation.method(#deleteCultivar, [id]),
            returnValue: Future<void>.value(),
            returnValueForMissingStub: Future<void>.value(),
          )
          as Future<void>);
  @override
  Future<dynamic> handleDioError(DioException? error) =>
      (super.noSuchMethod(
            Invocation.method(#handleDioError, [error]),
            returnValue: Future<dynamic>.value(),
          )
          as Future<dynamic>);
}
