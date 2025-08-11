import { CopyLinkAnim, PasteAnim, SaveFileAnim } from "./animated-steps"

export default function HowItWorks() {
  return (
    <section id="how-it-works" aria-label="How it works" className="border-t border-zinc-200 bg-white">
      <div className="container mx-auto max-w-5xl px-4 py-12 sm:py-16">
        <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">How it works</h2>
        <p className="mt-3 max-w-prose text-zinc-600">Three simple steps. No distractions, no signups.</p>

        <ol className="mt-8 grid gap-8 md:grid-cols-3">
          <li className="relative">
            <div className="mb-3 inline-flex h-8 w-8 items-center justify-center rounded-full bg-emerald-600 text-white">
              1
            </div>
            <h3 className="text-base font-semibold">Copy the link</h3>
            <p className="mt-1 text-sm text-zinc-600">From the video’s Share menu on YouTube.</p>
            <div className="mt-4">
              <CopyLinkAnim />
            </div>
          </li>

          <li className="relative">
            <div className="mb-3 inline-flex h-8 w-8 items-center justify-center rounded-full bg-emerald-600 text-white">
              2
            </div>
            <h3 className="text-base font-semibold">Paste it here</h3>
            <p className="mt-1 text-sm text-zinc-600">Drop it into the input and click download.</p>
            <div className="mt-4">
              <PasteAnim />
            </div>
          </li>

          <li className="relative">
            <div className="mb-3 inline-flex h-8 w-8 items-center justify-center rounded-full bg-emerald-600 text-white">
              3
            </div>
            <h3 className="text-base font-semibold">Save the file</h3>
            <p className="mt-1 text-sm text-zinc-600">Choose MP4 or MP3 and you’re done.</p>
            <div className="mt-4">
              <SaveFileAnim />
            </div>
          </li>
        </ol>
      </div>
    </section>
  )
}
