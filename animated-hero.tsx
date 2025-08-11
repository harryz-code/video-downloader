"use client"

import { useEffect, useRef, useState } from "react"

export default function AnimatedHero() {
  const ref = useRef<HTMLDivElement | null>(null)
  const [active, setActive] = useState(false)

  useEffect(() => {
    const node = ref.current
    if (!node) return
    let isVisible = false
    const onVisibility = () => setActive(isVisible && document.visibilityState === "visible")
    const io = new IntersectionObserver(
      (entries) => {
        isVisible = entries.some((e) => e.isIntersecting && e.intersectionRatio > 0.25)
        onVisibility()
      },
      { threshold: [0, 0.25, 0.5, 1] },
    )
    io.observe(node)
    document.addEventListener("visibilitychange", onVisibility)
    return () => {
      io.disconnect()
      document.removeEventListener("visibilitychange", onVisibility)
    }
  }, [])

  return (
    <div
      ref={ref}
      className="relative w-full overflow-hidden rounded-xl border border-zinc-200 bg-white shadow-sm"
      role="img"
      aria-label="Animated preview: paste link, choose quality, download, and watch progress"
    >
      <div className="aspect-[16/10] md:aspect-[16/9]">
        <svg viewBox="0 0 1280 720" className="h-full w-full">
          <defs>
            <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
              <path d="M 48 0 L 0 0 0 48" fill="none" stroke="#f1f5f9" strokeWidth="1" />
            </pattern>
            <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#34d399" stopOpacity="0.0" />
              <stop offset="50%" stopColor="#34d399" stopOpacity="0.45" />
              <stop offset="100%" stopColor="#34d399" stopOpacity="0.0" />
            </linearGradient>
          </defs>

          {/* Background */}
          <rect x="0" y="0" width="1280" height="720" fill="url(#grid)" />
          {/* Card */}
          <rect x="24" y="48" width="1232" height="616" rx="18" fill="#ffffff" stroke="#e5e7eb" />

          {/* Badges */}
          <g className={active ? "run badges" : "badges"}>
            <rect x="56" y="68" width="120" height="32" rx="16" fill="#ecfdf5" stroke="#bbf7d0" />
            <text x="76" y="89" fontFamily="system-ui, -apple-system" fontSize="14" fill="#065f46">
              100% Free
            </text>
            <rect x="186" y="68" width="150" height="32" rx="16" fill="#f8fafc" stroke="#e5e7eb" />
            <text x="204" y="89" fontFamily="system-ui, -apple-system" fontSize="14" fill="#475569">
              No Registration
            </text>
            <rect x="346" y="68" width="120" height="32" rx="16" fill="#f8fafc" stroke="#e5e7eb" />
            <text x="364" y="89" fontFamily="system-ui, -apple-system" fontSize="14" fill="#475569">
              HD Quality
            </text>
            <rect x="476" y="68" width="120" height="32" rx="16" fill="#f8fafc" stroke="#e5e7eb" />
            <text x="496" y="89" fontFamily="system-ui, -apple-system" fontSize="14" fill="#475569">
              MP4 Format
            </text>
          </g>

          {/* Info note (original height) */}
          <g className={active ? "run note" : "note"}>
            <rect x="56" y="116" width="1168" height="70" rx="14" fill="#ecfdf5" stroke="#bbf7d0" />
            <circle cx="84" cy="151" r="10" fill="#10b981" />
            <rect x="79" y="146" width="10" height="10" rx="2" fill="#ffffff" />
            <text x="106" y="146" fontFamily="system-ui, -apple-system" fontWeight="600" fontSize="16" fill="#065f46">
              Where are files saved?
            </text>
            <text x="106" y="166" fontFamily="system-ui, -apple-system" fontSize="14" fill="#065f46">
              Videos are automatically saved to your system&apos;s default Downloads folder. After completion, you can
              open the folder directly.
            </text>
          </g>

          {/* URL label + input (original size 60) with larger spacing above */}
          <text x="56" y="236" fontFamily="system-ui, -apple-system" fontWeight="600" fontSize="14" fill="#0f172a">
            YouTube Video URL
          </text>
          <rect x="56" y="256" width="1168" height="60" rx="14" fill="#ffffff" stroke="#e5e7eb" />
          <rect
            className={active ? "run shine" : "shine"}
            x="56"
            y="256"
            width="140"
            height="60"
            rx="14"
            fill="url(#shine)"
          />
          <g className={active ? "run ghost" : "ghost"}>
            <rect x="920" y="222" width="320" height="36" rx="10" fill="#10b981" opacity="0.12" />
            <text x="932" y="244" fontFamily="ui-monospace, SFMono-Regular, Menlo" fontSize="16" fill="#047857">
              https://youtu.be/VIDEO_ID
            </text>
          </g>
          <text
            x="82"
            y="292"
            className={active ? "run pasted" : "pasted"}
            fontFamily="ui-monospace, Menlo"
            fontSize="16"
            fill="#64748b"
          >
            https://www.youtube.com/watch?v=VIDEO_ID
          </text>

          {/* Quality label + select (original size 60) with bigger gap */}
          <text x="56" y="366" fontFamily="system-ui, -apple-system" fontWeight="600" fontSize="14" fill="#0f172a">
            Video Quality
          </text>
          <rect x="56" y="386" width="1168" height="60" rx="14" fill="#ffffff" stroke="#e5e7eb" />
          <text x="82" y="422" fontFamily="system-ui, -apple-system" fontSize="16" fill="#475569">
            Best Available
          </text>

          {/* CTA (original 56) with bigger gap below select */}
          <g className={active ? "run cta" : "cta"}>
            <rect x="56" y="488" width="1168" height="56" rx="14" fill="#10b981" />
            <text x="540" y="520" fontFamily="system-ui, -apple-system" fontWeight="700" fontSize="16" fill="#ffffff">
              DOWNLOAD VIDEO
            </text>
          </g>

          {/* Progress (original 12) positioned lower to fill card */}
          <rect x="56" y="580" width="1168" height="12" rx="6" fill="#f1f5f9" />
          <rect
            className={active ? "run progress" : "progress"}
            x="56"
            y="580"
            width="0"
            height="12"
            rx="6"
            fill="#10b981"
          />

          <style>
            {`
              .badges, .note, .shine, .ghost, .pasted, .cta, .progress { animation: none; }
              .run.badges, .run.note { animation: fadeIn 3.6s ease-in-out infinite; }
              .run.shine { animation: shine 3.6s ease-in-out infinite; }
              .run.ghost { animation: dropIn 3.6s ease-in-out infinite; }
              .run.pasted { animation: appear 3.6s ease-in-out infinite; }
              .run.cta { transform-origin: 640px 516px; animation: pulse 3.6s ease-in-out infinite; }
              .run.progress { animation: fill 3.6s ease-in-out infinite; }

              @keyframes fadeIn { 0%, 10% { opacity: 0; } 25%, 100% { opacity: 1; } }
              @keyframes shine {
                0% { transform: translateX(0); opacity: 0; }
                20% { opacity: .9; }
                50% { transform: translateX(1028px); opacity: .7; }
                60%,100% { opacity: 0; }
              }
              @keyframes dropIn {
                0% { transform: translate(0, -16px); opacity: 0; }
                18% { transform: translate(0, -6px); opacity: .95; }
                28% { transform: translate(-708px, 34px); opacity: 1; }
                32% { opacity: 0; }
                100% { opacity: 0; }
              }
              @keyframes appear { 0%, 30% { opacity: 0; } 40%, 100% { opacity: 1; } }
              @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.015); } }
              @keyframes fill { 0% { width: 0; } 70% { width: 1168px; } 100% { width: 1168px; } }

              @media (prefers-reduced-motion: reduce) {
                .run.badges, .run.note, .run.shine, .run.ghost, .run.pasted, .run.cta, .run.progress {
                  animation: none !important;
                }
              }
            `}
          </style>
        </svg>
      </div>
    </div>
  )
}
