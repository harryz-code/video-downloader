import { CircleDollarSign, Lock, MonitorSmartphone, Timer } from "lucide-react"

export default function FeatureCards() {
  // Removed "Minimal, elegant UI" as requested
  const items = [
    {
      title: "100% Free",
      desc: "Always free to use. No signups or paywalls.",
      icon: CircleDollarSign,
      alt: "Dollar sign icon indicating the app is free",
    },
    {
      title: "Fast by default",
      desc: "Optimized flows so you get your video in just a few clicks.",
      icon: Timer,
      alt: "Timer icon representing speed",
    },
    {
      title: "Mobile‑first",
      desc: "Works beautifully on phones, tablets, and desktops.",
      icon: MonitorSmartphone,
      alt: "Device icon showing mobile and desktop compatibility",
    },
    {
      title: "Privacy‑friendly",
      desc: "We respect your privacy. No unnecessary tracking.",
      icon: Lock,
      alt: "Padlock icon representing privacy and safety",
    },
  ]

  return (
    <section id="features" aria-label="Features" className="border-t border-zinc-200 bg-white">
      <div className="container mx-auto max-w-6xl px-4 py-12 sm:py-16">
        <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">Features that matter</h2>
        <p className="mt-3 max-w-prose text-zinc-600">
          Designed for clarity and speed, so you can focus on the content you love.
        </p>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {items.map((item, idx) => {
            const Icon = item.icon
            return (
              <div
                key={idx}
                className="rounded-lg border border-zinc-200 bg-white p-6 text-center transition-colors hover:border-emerald-200"
              >
                <div className="mx-auto mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-100">
                  <Icon className="h-5 w-5" aria-label={item.alt} />
                </div>
                <h3 className="text-base font-semibold">{item.title}</h3>
                <p className="mt-2 text-sm text-zinc-600">{item.desc}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
