import 'package:jaspr/server.dart';
import 'package:jaspr/dom.dart';
import 'pages/landing_page.dart';

void main() {
  Jaspr.initializeApp();

  runApp(Document(
    title: 'CultivAR',
    styles: [
      css.import(
          'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap'),
      css('body').styles(
        margin: Margin.all(0.px),
        padding: Padding.all(0.px),
        fontFamily: const FontFamily.list(
            [FontFamily('Inter'), FontFamily('sans-serif')]),
        backgroundColor: Color('#050505'),
        color: Color('#FFFFFF'),
      ),
    ],
    body: const LandingPage(),
  ));
}
