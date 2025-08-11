import Link from "next/link"
import { Button } from "@/components/ui/button"
import AnimatedHero from "./animated-hero"

export default function Hero() {
  return (
    <section aria-label="Intro" className="relative overflow-hidden border-b border-zinc-200 bg-white">
      <div className="container mx-auto grid max-w-6xl grid-cols-1 items-center gap-10 px-4 py-12 sm:py-16 md:grid-cols-2">
        <div>
          <h1 className="text-pretty text-3xl font-semibold leading-tight tracking-tight sm:text-4xl">
            Free YouTube Video Downloader
          </h1>
          <p className="mt-3 max-w-prose text-zinc-600">Free. Fast. Private. No registration required.</p>

          <div className="mt-6 flex flex-wrap items-center gap-3">
            <Button asChild className="bg-emerald-600 hover:bg-emerald-700 text-white">
              <Link href="#downloader" aria-label="Jump to downloader">
                Start downloading
              </Link>
            </Button>
            <Button asChild variant="outline" className="border-zinc-300 hover:bg-zinc-50 bg-transparent">
              <Link href="#how-it-works" aria-label="Learn how it works">
                Learn more
              </Link>
            </Button>
          </div>
        </div>

        <div className="relative">
          <AnimatedHero />
        </div>
      </div>
    </section>
  )
}
