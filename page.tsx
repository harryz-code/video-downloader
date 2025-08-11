import type { Metadata } from "next"
import SiteHeader from "@/components/site-header"
import Hero from "@/components/hero"
import UrlForm from "@/components/url-form"
import FeatureCards from "@/components/feature-cards"
import HowItWorks from "@/components/how-it-works"
import Faq from "@/components/faq"
import Footer from "@/components/footer"
import JsonLd from "@/components/json-ld"

export const metadata: Metadata = {
  title: "Free YouTube Video Downloader — Fast, Private, Minimal",
  description:
    "Download YouTube videos quickly with a clean, elegant interface. Mobile-first, privacy-friendly, and completely free.",
  keywords: [
    "Free YouTube video downloader",
    "YouTube downloader",
    "download YouTube video",
    "MP4 downloader",
    "MP3 converter",
  ],
  alternates: { canonical: "https://yourdomain.com/" },
  openGraph: {
    title: "Free YouTube Video Downloader — Fast, Private, Minimal",
    description:
      "Download YouTube videos quickly with a clean, elegant interface. Mobile-first, privacy-friendly, and free.",
    url: "https://yourdomain.com/",
    siteName: "YT Downloader",
    images: [{ url: "/og-image.png", width: 1200, height: 630, alt: "Preview of YT Downloader interface" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Free YouTube Video Downloader — Fast, Private, Minimal",
    description:
      "Download YouTube videos quickly with a clean, elegant interface. Mobile-first, privacy-friendly, and free.",
    images: ["/og-image.png"],
  },
  robots: { index: true, follow: true },
}

export default function Page() {
  return (
    <>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-emerald-600 focus:px-3 focus:py-2 focus:text-white focus:shadow"
      >
        Skip to content
      </a>

      <SiteHeader />
      <main id="main" role="main">
        <Hero />

        {/* Downloader section with header + badges styled to match the reference while keeping emerald branding */}
        <section id="downloader" aria-label="YouTube video downloader" className="bg-white">
          <div className="container mx-auto max-w-3xl px-4 py-12 sm:py-16">
            <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">Paste link. Download instantly.</h2>
            <p className="mt-3 max-w-prose text-zinc-600">
              100% free, no registration. Choose MP4 or MP3 and get your file in seconds.
            </p>

            {/* Badges */}
            <div className="mt-4 flex flex-wrap gap-2" role="list" aria-label="Key highlights">
              <span
                role="listitem"
                className="inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700"
              >
                100% Free
              </span>
              <span
                role="listitem"
                className="inline-flex items-center rounded-full border border-zinc-200 bg-zinc-50 px-3 py-1 text-xs font-medium text-zinc-700"
              >
                No Registration
              </span>
              <span
                role="listitem"
                className="inline-flex items-center rounded-full border border-zinc-200 bg-zinc-50 px-3 py-1 text-xs font-medium text-zinc-700"
              >
                HD Quality
              </span>
              <span
                role="listitem"
                className="inline-flex items-center rounded-full border border-zinc-200 bg-zinc-50 px-3 py-1 text-xs font-medium text-zinc-700"
              >
                MP4 Format
              </span>
            </div>

            {/* Framed form container */}
            <div className="mt-6 rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
              <UrlForm />
            </div>
          </div>
        </section>

        <FeatureCards />
        <HowItWorks />
        <Faq />
      </main>
      <Footer />
      <JsonLd />
    </>
  )
}
