import type { Metadata } from 'next';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export const metadata: Metadata = {
  title: 'Authentication',
  description: 'Sign in or sign up to access Bazov',
};

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <main className="flex flex-1 flex-col items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}
