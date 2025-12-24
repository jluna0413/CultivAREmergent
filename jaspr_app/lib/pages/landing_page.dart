import 'package:jaspr/jaspr.dart';
import 'package:jaspr/dom.dart';
import '../components/feature_section.dart';

class LandingPage extends StatelessComponent {
  const LandingPage({super.key});

  @override
  Component build(BuildContext context) {
    return div(
      // Children list
      [
        // Immersive Background (Hero Image with Overlay)
        div([],
            styles: Styles(
              position: Position.fixed(
                  top: 0.px, left: 0.px, right: 0.px, bottom: 0.px),
              zIndex: ZIndex(-2),
            ),
            attributes: {
              'style': '''
            background: linear-gradient(to bottom, rgba(0,0,0,0.3), #000000), url(images/hero.png) no-repeat center center;
            background-size: cover;
          '''
            }),

        // --- HERO SECTION ---
        div([
          // Logo
          div(
              [
                div([text('🌿')],
                    styles: Styles(
                      width: 100.px,
                      height: 100.px,
                      radius: BorderRadius.circular(50.px),
                      border:
                          Border.all(color: Color('#ffffff').withOpacity(0.2)),
                      display: Display.flex,
                      alignItems: AlignItems.center,
                      justifyContent: JustifyContent.center,
                      fontSize: 3.rem,
                    ),
                    attributes: {
                      'style':
                          'background: linear-gradient(to bottom right, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); backdrop-filter: blur(5px);'
                    }),
              ],
              styles: Styles(
                margin: Margin.only(bottom: 3.rem),
              ),
              attributes: {
                'style':
                    'filter: drop-shadow(0px 10px 20px rgba(34, 197, 94, 0.3));'
              }),

          // Main Headline
          h1(
              [
                text('Genetic '),
                span([
                  text('Excellence')
                ], attributes: {
                  'style':
                      'background: linear-gradient(to right, #4ade80, #22c55e); -webkit-background-clip: text; background-clip: text; color: transparent;'
                }),
              ],
              styles: Styles(
                fontSize: 5.rem,
                fontWeight: FontWeight.w800,
                margin: Margin.only(bottom: 1.5.rem),
                textShadow:
                    Shadow(blur: 20.px, color: Color('rgba(0,0,0,0.5)')),
              ),
              attributes: {'style': 'letter-spacing: -2px; line-height: 1.1;'}),

          // Subheadline
          p(
              [
                text(
                    'Cultivate intelligence with the world\'s most advanced grow platform.\nPrecision analytics for the modern breeder.')
              ],
              styles: Styles(
                fontSize: 1.25.rem,
                color: Color('#e5e5e5'),
                maxWidth: 600.px,
                margin: Margin.only(bottom: 4.rem),
                textShadow:
                    Shadow(blur: 10.px, color: Color('rgba(0,0,0,0.8)')),
              ),
              attributes: {'style': 'line-height: 1.6;'}),

          // Call to Action
          div([
            a([text('Get Started')],
                href: '#',
                styles: Styles(
                  padding:
                      Padding.symmetric(horizontal: 2.5.rem, vertical: 1.rem),
                  radius: BorderRadius.circular(9999.px),
                  color: Color('#ffffff'),
                  fontWeight: FontWeight.w600,
                  fontSize: 1.1.rem,
                  textDecoration: TextDecoration.none,
                  shadow: BoxShadow(
                      offsetX: 0.px,
                      offsetY: 4.px,
                      blur: 12.px,
                      color: Color('#22c55e').withOpacity(0.4)),
                  transition:
                      Transition('all', duration: Duration(milliseconds: 200)),
                ),
                attributes: {
                  'style':
                      'background: linear-gradient(to right, #22c55e, #16a34a);'
                }),
          ],
              styles: Styles(
                display: Display.flex,
                gap: Gap.all(1.5.rem),
                flexWrap: FlexWrap.wrap,
                justifyContent: JustifyContent.center,
              )),

          // Scroll hint
          div([
            text('Scroll to explore'),
            div([],
                styles: Styles(
                    width: 1.px,
                    height: 40.px,
                    backgroundColor: Color('#ffffff'),
                    margin: Margin.only(top: 1.rem))),
          ],
              styles: Styles(
                opacity: 0.5,
                fontSize: 0.9.rem,
                display: Display.flex,
                flexDirection: FlexDirection.column,
                alignItems: AlignItems.center,
                margin: Margin.only(top: 10.rem),
              )),
        ],
            styles: Styles(
              display: Display.flex,
              flexDirection: FlexDirection.column,
              alignItems: AlignItems.center,
              justifyContent: JustifyContent.center,
              minHeight: 100.vh,
              padding: Padding.symmetric(horizontal: 2.rem),
              textAlign: TextAlign.center,
              color: Color('#ffffff'),
              fontFamily: FontFamily.list(
                  [FontFamily('Inter'), FontFamily('sans-serif')]),
            )),

        // --- FEATURES ---

        // 1. Precision Analytics
        FeatureSection(
          title: 'Data-Driven Causality',
          description:
              'Move beyond intuition. Our sensor fusion engine correlates environmental variables with phenotypic expression in real-time. Understand exactly what inputs yield your best results.',
          isReversed: false,
          visualContent: img(
              src: 'images/analytics.png',
              styles: Styles(
                  width: 100.percent,
                  height: 100.percent,
                  radius: BorderRadius.circular(20.px),
                  objectFit: ObjectFit.cover)),
        ),

        // 2. Genetic Lineage
        FeatureSection(
          title: 'Trace Every Trait',
          description:
              'The world\'s first immutable ledger for plant genetics. Track generations, verify parents, and secure your intellectual property with cryptographic certainty.',
          isReversed: true,
          visualContent: img(
              src: 'images/genetics.png',
              styles: Styles(
                  width: 100.percent,
                  height: 100.percent,
                  radius: BorderRadius.circular(20.px),
                  objectFit: ObjectFit.cover)),
        ),

        // 3. Environmental Control
        FeatureSection(
          title: 'God Mode for Your Grow',
          description:
              'Automate light cycles, VPD targets, and nutrient dosing. Our hardware-agnostic platform integrates with your existing IoT devices for seamless control.',
          isReversed: false,
          visualContent: img(
              src: 'images/environment.png',
              styles: Styles(
                  width: 100.percent,
                  height: 100.percent,
                  radius: BorderRadius.circular(20.px),
                  objectFit: ObjectFit.cover)),
        ),

        // 4. Marketplace
        FeatureSection(
          title: 'The Circuit',
          description:
              'Trade seeds, clones, and pollen with confidence. Our decentralized marketplace uses Soul-Bound Tokens (SBTs) to ensure provenance is never lost.',
          isReversed: true,
          visualContent: img(
              src: 'images/marketplace.png',
              styles: Styles(
                  width: 100.percent,
                  height: 100.percent,
                  radius: BorderRadius.circular(20.px),
                  objectFit: ObjectFit.cover),
              attributes: {'onerror': 'this.style.display="none"'}),
        ),

        // Footer Placeholder
        div(
            [
              text('© 2025 CultivAR. All rights reserved.'),
            ],
            styles: Styles(
              padding: Padding.all(4.rem),
              textAlign: TextAlign.center,
              color: Color('#888888'),
            ),
            attributes: {
              'style': 'border-top: 1px solid rgba(255,255,255,0.1);'
            }),
      ],

      // Wrapper styles
      classes: 'landing-page',
    );
  }
}
