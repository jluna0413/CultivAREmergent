# Flutter UI Guidelines for CultivAR

## Design System

Map styles from web styles.css:
- --color-primary → AppColors.primary (shades: 50-900)
- --color-secondary → AppColors.secondary
- Typography: AppTypography (headings H1-H6, body, caption)
- Spacing: AppSpacing (4, 8, 16, 24, 32, 48, 64)
- Border radius: 8, 12, 16, 24

## Components

### CustomButton

Variants:
- primary: gradient ElevatedButton.styleFrom(
  background: LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]),
  foregroundColor: Colors.white,
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))
)
- secondary: ElevatedButton.styleFrom(background: AppColors.secondary, foregroundColor: Colors.white)
- outline: OutlinedButton.styleFrom(side: BorderSide(color: AppColors.primary))

Props: onPressed, child Text, loading: bool (show CircularProgressIndicator)

Usage:
CustomButton.primary(
  'Login',
  onPressed: _login,
  loading: isLoading,
);

### GlassCard

Glassmorphism card:
Container(
  decoration: BoxDecoration(
    borderRadius: BorderRadius.circular(16),
    border: Border.all(color: Colors.white.withOpacity(0.2)),
    gradient: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [
        Colors.white.withOpacity(0.1),
        Colors.white.withOpacity(0.05),
      ],
    ),
    boxShadow: [
      BoxShadow(
        color: Colors.black.withOpacity(0.1),
        blurRadius: 10,
        offset: const Offset(0, 5),
      ),
    ],
  ),
  child: Padding(padding: EdgeInsets.all(16), child: content),
)

### LoadingIndicator

Centered CircularProgressIndicator(color: AppColors.primary)

### ErrorView

Column(
  children: [
    Icon(Icons.error, color: Colors.red, size: 64),
    Text(error, style: TextStyle(color: Colors.white)),
    CustomButton.outline('Retry', onPressed: onRetry),
  ],
)

## Patterns

### Navigation

GoRouter guards:
GoRouter(
  redirect: (context, state) {
    final isAuth = ref.read(authNotifierProvider).isAuthenticated;
    final isLogin = state.location == '/login';
    if (!isAuth && !isLogin) return '/login';
    if (isAuth && isLogin) return '/dashboard';
    return null;
  },
)

### State Management

ref.watch(provider).when(
  data: (data) => ListView.builder(itemBuilder: (context, index) => PlantCard(plant: data[index])),
  loading: () => LoadingIndicator(),
  error: (error, stack) => ErrorView(error),
);

### Forms

GlobalKey<FormState> formKey = GlobalKey<FormState>();

CustomTextField(
  validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
);

### Animations

Hero(tag: 'plant_image_${plant.id}'),
PageRouteBuilder(pageBuilder: (context, animation, secondaryAnimation) => NewScreen(), transitionsBuilder: ...)

### Accessibility

Semantics(label: 'Plant Name', child: Text(plant.name))
Ensure contrast ratios >4.5:1

### Theming

ThemeData(
  colorScheme: ColorScheme.dark(primary: AppColors.primary),
  useMaterial3: true,
)

### Performance

- const constructors
- ListView.builder
- CachedNetworkImage for images
- RepaintBoundary for complex widgets