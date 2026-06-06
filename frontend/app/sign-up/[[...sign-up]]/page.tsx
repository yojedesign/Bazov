import { SignUp } from '@clerk/nextjs';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Sign Up',
  description: 'Create your Bazov account',
};

export default function SignUpPage() {
  return (
    <div className="w-full max-w-md mx-auto">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">
          Create your account
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Join Bazov to start mapping your professional relationships
        </p>
      </div>
      
      <SignUp
        path="/sign-up"
        routing="path"
        signInUrl="/sign-in"
        afterSignUpUrl="/dashboard/onboarding"
        appearance={{
          elements: {
            rootBox: {
              width: '100%',
            },
            card: {
              boxShadow: 'none',
              border: '1px solid hsl(var(--border))',
            },
            headerTitle: {
              fontSize: '1.5rem',
              fontWeight: 600,
            },
            headerSubtitle: {
              color: 'hsl(var(--muted-foreground))',
            },
            socialButtonsBlockButton: {
              backgroundColor: 'hsl(var(--background))',
              border: '1px solid hsl(var(--border))',
              color: 'hsl(var(--foreground))',
              '&:hover': {
                backgroundColor: 'hsl(var(--muted))',
              },
            },
            formButtonPrimary: {
              backgroundColor: 'hsl(var(--primary))',
              color: 'hsl(var(--primary-foreground))',
              '&:hover': {
                backgroundColor: 'hsl(var(--primary))',
                opacity: 0.9,
              },
            },
            formFieldInput: {
              backgroundColor: 'hsl(var(--background))',
              border: '1px solid hsl(var(--border))',
              color: 'hsl(var(--foreground))',
              '&:focus': {
                borderColor: 'hsl(var(--ring))',
                boxShadow: '0 0 0 1px hsl(var(--ring))',
              },
            },
            formFieldLabel: {
              color: 'hsl(var(--foreground))',
            },
            footerActionLink: {
              color: 'hsl(var(--primary))',
              '&:hover': {
                color: 'hsl(var(--primary))',
                opacity: 0.8,
              },
            },
          },
        }}
      />
    </div>
  );
}
