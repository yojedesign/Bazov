import type { Metadata, Viewport } from 'next';
import { ClerkProvider } from '@clerk/nextjs';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    default: 'Bazov - Relationship Intelligence Platform',
    template: '%s | Bazov',
  },
  description: 'Crawl, analyze, and map professional relationships with AI-powered insights.',
  keywords: ['relationships', 'intelligence', 'crawling', 'linkedin', 'networking', 'business'],
  authors: [{ name: 'Bazov Team' }],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://bazov.yojedesign.com',
    siteName: 'Bazov',
    title: 'Bazov - Relationship Intelligence Platform',
    description: 'Crawl, analyze, and map professional relationships with AI-powered insights.',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Bazov - Relationship Intelligence Platform',
    description: 'Crawl, analyze, and map professional relationships with AI-powered insights.',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: 'white' },
    { media: '(prefers-color-scheme: dark)', color: 'black' },
  ],
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <ClerkProvider
      appearance={{
        layout: {
          logoImageUrl: '/logo.svg',
          logoPlacement: 'inside',
        },
        variables: {
          colorPrimary: '#000000',
          colorBackground: '#ffffff',
          colorText: '#000000',
        },
      }}
    >
      <html lang="en" suppressHydrationWarning>
        <body className={`${inter.className} antialiased`}>
          <div className="relative flex min-h-screen flex-col">
            {children}
          </div>
        </body>
      </html>
    </ClerkProvider>
  );
}
