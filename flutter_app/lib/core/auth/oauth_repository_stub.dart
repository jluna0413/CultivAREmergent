import 'oauth_repository_base.dart';

OAuthRepository getPlatformOAuthRepository() {
  throw UnsupportedError(
    'Cannot create OAuthRepository without dart:html or dart:io',
  );
}
