import 'package:json_annotation/json_annotation.dart';

/// Simple generic paginated response model used for mapping API responses
class PaginatedResponse<T> {
  PaginatedResponse({
    required this.items,
    required this.total,
    required this.page,
    required this.size,
    required this.pages,
    required this.hasNext,
    required this.hasPrev,
  });

  final List<T> items;
  final int total;
  final int page;
  final int size;
  final int pages;
  final bool hasNext;
  final bool hasPrev;
}

class PaginatedResponseConverter<T>
    implements JsonConverter<PaginatedResponse<T>, Map<String, dynamic>> {
  /// Constructor accepts a function to parse a T from JSON
  const PaginatedResponseConverter(this._fromJson);

  final T Function(Map<String, dynamic>) _fromJson;

  T fromJsonT(Map<String, dynamic> json) => _fromJson(json);

  @override
  PaginatedResponse<T> fromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List)
        .map((e) => fromJsonT(e as Map<String, dynamic>))
        .toList();
    return PaginatedResponse(
      items: items,
      total: json['total'] as int,
      page: json['page'] as int,
      size: json['size'] as int,
      pages: json['pages'] as int,
      hasNext: json['has_next'] as bool? ?? false,
      hasPrev: json['has_prev'] as bool? ?? false,
    );
  }

  @override
  Map<String, dynamic> toJson(PaginatedResponse<T> object) {
    // This is not needed for this use case.
    throw UnimplementedError();
  }
}
