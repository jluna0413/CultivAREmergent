import 'package:jaspr/jaspr.dart';
import 'package:jaspr/dom.dart';

class FeatureSection extends StatelessComponent {
  final String title;
  final String description;
  final String imageUrl;
  final bool isReversed;
  final Component? visualContent;

  const FeatureSection({
    required this.title,
    required this.description,
    this.imageUrl = '',
    this.isReversed = false,
    this.visualContent,
    super.key,
  });

  @override
  Component build(BuildContext context) {
    return div(
        classes: 'feature-section',
        styles: Styles(
          display: Display.flex,
          flexWrap: FlexWrap.wrap,
          alignItems: AlignItems.center,
          justifyContent: JustifyContent.center,
          padding: Padding.symmetric(vertical: 4.rem, horizontal: 1.5.rem),
          minHeight: 60.vh,
        ),
        attributes: {
          'style': 'flex-direction: ${isReversed ? 'row-reverse' : 'row'};'
        },
        [
          // Text Content
          div(
              styles: Styles(
                // Removed FlexBasis usage to avoid analyzer error.
                // Using flex shorthand or separate properties if needed.
                flex: Flex(grow: 1, shrink: 1),
                minWidth: 300.px,
                maxWidth: 600.px,
                textAlign: TextAlign.left,
                padding: Padding.all(2.rem),
              ),
              [
                h2([text(title)],
                    styles: Styles(
                      fontSize: 2.5.rem,
                      fontWeight: FontWeight.w700,
                      color: Color('#f0fdf4'),
                      margin: Margin.only(bottom: 1.rem),
                    ),
                    attributes: {
                      'style':
                          'background: linear-gradient(to right, #ffffff, #86efac); -webkit-background-clip: text; background-clip: text; color: transparent;'
                    }),
                p([text(description)],
                    styles: Styles(
                      fontSize: 1.1.rem,
                      color: Color('#a3a3a3'),
                      lineHeight: Unit.em(1.6),
                    )),
              ]),

          // Visual Content
          div(
              styles: Styles(
                flex: Flex(grow: 1, shrink: 1),
                width: 100.percent,
                maxWidth: 500.px,
                height: 300.px,
                radius: BorderRadius.circular(20.px),
                border: Border.all(color: Color('#ffffff').withOpacity(0.1)),
                display: Display.flex,
                alignItems: AlignItems.center,
                justifyContent: JustifyContent.center,
                margin: Margin.all(2.rem),
              ),
              attributes: {
                'style':
                    'background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); box-shadow: 0 20px 50px rgba(0,0,0,0.5);'
              },
              [
                visualContent ??
                    div([],
                        styles: Styles(
                          width: 100.percent,
                          height: 100.percent,
                          radius: BorderRadius.circular(20.px),
                        ),
                        attributes: {
                          'style':
                              'background: linear-gradient(135deg, ${isReversed ? 'rgba(34, 197, 94, 0.1)' : 'rgba(34, 197, 94, 0.05)'}, transparent);'
                        })
              ]),
        ]);
  }
}
