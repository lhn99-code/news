import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'daramzi-pomodoro',
  web: {
    host: 'localhost',
    port: 3000,
    commands: {
      dev: 'rsbuild dev',
      build: 'rsbuild build',
    },
  },
  // 리워드 광고 등 권한이 필요한 기능을 쓰면 여기에 추가해요.
  // 예: ['ad'] — 실제 권한 키는 앱인토스 콘솔/문서 기준으로 확인 후 기입.
  permissions: [],
  outdir: 'dist',
  brand: {
    displayName: '다람쥐 뽀모도로',
    // TODO: 콘솔에 업로드할 실제 앱 아이콘 URL로 교체하세요.
    icon: 'https://static.toss.im/appsintoss/73/10550764-5ac1-44e2-9ff3-ad78d8d2e71a.png',
    primaryColor: '#3182F6',
    bridgeColorMode: 'inverted',
  },
  webViewProps: {
    type: 'partner',
  },
});
