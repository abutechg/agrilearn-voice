import "./globals.css";

export const metadata = {
  title: "AgriLearn Voice",
  description: "A voice-first agricultural learning assistant.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en"><body>{children}</body></html>
  );
}
