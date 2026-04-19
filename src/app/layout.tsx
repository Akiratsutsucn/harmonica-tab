import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "口琴练习",
  description: "个人口琴练习工具 - 边看谱边听歌",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="bg-warm-50 text-warm-800 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
