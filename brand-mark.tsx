import { Download, Play } from "lucide-react"

type Props = {
  className?: string
}

/**
 * A simple, premium-feel logo mark using lucide icons (no custom SVG).
 * Play triangle overlays a small download badge to convey "download videos".
 */
export default function BrandMark({ className }: Props) {
  return (
    <div
      className={[
        "relative grid place-items-center rounded-xl bg-gradient-to-br from-emerald-600 to-emerald-500 text-white shadow-sm ring-1 ring-emerald-300/60",
        className ?? "h-9 w-9",
      ].join(" ")}
      role="img"
      aria-label="YT Downloader logo: play triangle with download arrow"
    >
      <Play className="h-4.5 w-4.5 opacity-95" aria-hidden="true" />
      <div className="absolute -bottom-0.5 -right-0.5 grid h-3.5 w-3.5 place-items-center rounded-full bg-white text-emerald-600 ring-1 ring-emerald-200">
        <Download className="h-2.5 w-2.5" aria-hidden="true" />
      </div>
    </div>
  )
}
