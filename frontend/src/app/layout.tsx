import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Policy Deliberation System",
  description: "Multi-agent policy analysis with real-time visualization and SHAP/LIME explainability",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
