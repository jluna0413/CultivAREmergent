import 'oauth_repository_stub.dart'
    if (dart.library.io) 'oauth_repository_non_web.dart'
    if (dart.library.html) 'oauth_repository_web.dart';

import 'oauth_repository_base.dart';
export 'oauth_repository_base.dart';

// This factory function conditionally returns the correct platform-specific implementation
OAuthRepository getOAuthRepository() {
  return getPlatformOAuthRepository();
}
