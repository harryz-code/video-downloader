import type React from "react"

/**
 * Lightweight, dependency-free SVG animations for the "How it works" section.
 * - Accessible: role="img" + aria-label
 * - Respect reduced motion: animations pause when prefers-reduced-motion is set
 * - Responsive: SVG scales to container; wrapper uses aspect ratio and Tailwind utilities
 */

type BoxProps = {
  ariaLabel: string
  children: React.ReactNode
}

function Frame({ ariaLabel, children }: BoxProps) {
  return (
    <div
      className="relative w-full overflow-hidden rounded-lg border border-zinc-200 bg-zinc-50 shadow-sm"
      role="img"
      aria-label={ariaLabel}
    >
      <div className="aspect-[16/12]">{children}</div>
    </div>
  )
}

export function CopyLinkAnim() {
  return (
    <Frame ariaLabel="Animation showing copying a YouTube link from the Share menu">
      <svg viewBox="0 0 640 480" className="h-full w-full">
        <defs>
          <linearGradient id="glow" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0%" stopColor="#34d399" stopOpacity="0.15" />
            <stop offset="50%" stopColor="#34d399" stopOpacity="0.35" />
            <stop offset="100%" stopColor="#34d399" stopOpacity="0.15" />
          </linearGradient>
        </defs>

        {/* Window frame */}
        <rect x="24" y="24" width="592" height="432" rx="14" fill="white" stroke="#e5e7eb" />
        {/* Top bar */}
        <rect x="24" y="24" width="592" height="46" rx="14" fill="#f6f7f8" />
        <circle cx="48" cy="47" r="6" fill="#ef4444" />
        <circle cx="68" cy="47" r="6" fill="#f59e0b" />
        <circle cx="88" cy="47" r="6" fill="#10b981" />

        {/* YouTube thumbnail mock */}
        <rect x="48" y="92" width="280" height="158" rx="10" fill="#f3f4f6" stroke="#e5e7eb" />
        <polygon points="168,150 168,192 208,171" fill="#ef4444" />

        {/* Share button */}
        <rect x="348" y="212" width="110" height="30" rx="8" fill="#f3f4f6" stroke="#e5e7eb" />
        <text x="355" y="232" fontFamily="system-ui, -apple-system, Segoe UI, Roboto" fontSize="14" fill="#374151">
          Share
        </text>

        {/* URL pill that pulses */}
        <g className="url-pill">
          <rect x="48" y="280" width="544" height="40" rx="20" fill="url(#glow)" />
          <rect x="48" y="280" width="544" height="40" rx="20" fill="#ffffff" stroke="#e5e7eb" />
          <text x="68" y="305" fontFamily="ui-monospace, SFMono-Regular, Menlo" fontSize="14" fill="#6b7280">
            https://youtu.be/VIDEO_ID
          </text>
        </g>

        {/* Copy icon moves from URL to clipboard */}
        <g className="copy-seq">
          {/* Copy icon */}
          <rect className="copy-icon" x="540" y="288" width="24" height="24" rx="6" fill="#10b981" />
          <path d="M548 295h10v10h-10zM546 297h10" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" fill="none" />
          {/* Clipboard target */}
          <g className="clipboard">
            <rect x="500" y="340" width="40" height="48" rx="6" fill="#e5f7f1" stroke="#10b981" />
            <rect x="510" y="334" width="20" height="10" rx="3" fill="#10b981" />
            <polyline points="510,362 522,374 540,352" fill="none" stroke="#10b981" strokeWidth="3" />
          </g>
        </g>

        <style>
          {`
          .url-pill { animation: pulse 2.8s ease-in-out infinite; }
          .copy-icon { animation: moveCopy 2.8s ease-in-out infinite; }
          .clipboard { opacity: 0; animation: showClip 2.8s ease-in-out infinite; }

          @keyframes pulse {
            0%, 100% { opacity: 1; }
            40% { opacity: 0.9; }
            50% { opacity: 1; }
          }
          @keyframes moveCopy {
            0%   { transform: translate(0px, 0px) scale(1); opacity: 0; }
            20%  { opacity: 1; }
            45%  { transform: translate(-40px, 52px) scale(1); }
            55%  { transform: translate(-40px, 52px) scale(0.92); }
            65%  { transform: translate(-40px, 52px) scale(1); opacity: 1; }
            80%  { opacity: 0; }
            100% { opacity: 0; }
          }
          @keyframes showClip {
            0%, 40% { opacity: 0; }
            55%, 100% { opacity: 1; }
          }

          @media (prefers-reduced-motion: reduce) {
            .url-pill, .copy-icon, .clipboard { animation: none !important; }
          }
        `}
        </style>
      </svg>
    </Frame>
  )
}

export function PasteAnim() {
  return (
    <Frame ariaLabel="Animation showing pasting a link into the downloader input">
      <svg viewBox="0 0 640 480" className="h-full w-full">
        {/* Input field */}
        <rect x="40" y="180" width="560" height="50" rx="14" fill="#ffffff" stroke="#e5e7eb" />
        {/* Caret */}
        <rect className="caret" x="60" y="190" width="2.5" height="30" fill="#10b981" />
        {/* Ghost link moving into input */}
        <g className="ghost-link">
          <rect x="220" y="110" width="220" height="34" rx="8" fill="#10b981" opacity="0.1" />
          <text x="232" y="132" fontFamily="ui-monospace, SFMono-Regular, Menlo" fontSize="14" fill="#047857">
            https://youtu.be/VIDEO_ID
          </text>
        </g>
        {/* Final pasted text */}
        <text
          className="pasted"
          x="70"
          y="210"
          fontFamily="ui-monospace, SFMono-Regular, Menlo"
          fontSize="14"
          fill="#6b7280"
        >
          https://youtu.be/VIDEO_ID
        </text>

        {/* Download button highlight */}
        <rect x="200" y="260" width="240" height="44" rx="10" className="cta" />
        <text x="240" y="288" fontFamily="system-ui, -apple-system" fontWeight="600" fontSize="16" fill="#ffffff">
          DOWNLOAD
        </text>

        <style>
          {`
          .ghost-link { animation: dropIn 3s ease-in-out infinite; }
          .pasted { opacity: 0; animation: showText 3s ease-in-out infinite; }
          .caret { animation: blink .9s steps(1) infinite; }
          .cta { fill: #10b981; opacity: 0.85; animation: pulseCta 3s ease-in-out infinite; }

          @keyframes dropIn {
            0%   { transform: translate(0, -22px); opacity: 0; }
            20%  { transform: translate(0, -8px); opacity: .9; }
            35%  { transform: translate(-160px, 90px); opacity: .95; }
            40%  { opacity: 0; }
            100% { opacity: 0; }
          }
          @keyframes showText {
            0%, 35% { opacity: 0; }
            45%, 100% { opacity: 1; }
          }
          @keyframes blink {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0; }
          }
          @keyframes pulseCta {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.015); }
          }

          @media (prefers-reduced-motion: reduce) {
            .ghost-link, .pasted, .caret, .cta { animation: none !important; }
          }
        `}
        </style>
      </svg>
    </Frame>
  )
}

export function SaveFileAnim() {
  return (
    <Frame ariaLabel="Animation showing a progress bar completing and a file being saved">
      <svg viewBox="0 0 640 480" className="h-full w-full">
        {/* File icon */}
        <g className="file">
          <rect x="290" y="110" width="60" height="76" rx="8" fill="#e5f7f1" stroke="#10b981" />
          <polyline points="290,125 320,125 335,140 335,186 290,186" fill="none" stroke="#10b981" strokeWidth="2" />
        </g>

        {/* Progress track */}
        <rect x="120" y="260" width="400" height="16" rx="8" fill="#f3f4f6" />
        {/* Progress fill */}
        <rect className="progress" x="120" y="260" width="0" height="16" rx="8" fill="#10b981" />

        {/* Check circle */}
        <g className="check">
          <circle cx="320" cy="300" r="20" fill="#10b981" />
          <polyline
            points="312,300 320,308 332,292"
            fill="none"
            stroke="#ffffff"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </g>

        <style>
          {`
          .progress { animation: fill 3s ease-in-out infinite; }
          .check { transform-origin: 320px 300px; opacity: 0; animation: pop 3s ease-in-out infinite; }
          .file { transform-origin: 320px 148px; animation: float 3s ease-in-out infinite; }

          @keyframes fill {
            0% { width: 0px; }
            70% { width: 400px; }
            75%, 100% { width: 400px; }
          }
          @keyframes pop {
            0%, 70% { opacity: 0; transform: scale(.8); }
            78% { opacity: 1; transform: scale(1.05); }
            100% { opacity: 1; transform: scale(1); }
          }
          @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-4px); }
          }

          @media (prefers-reduced-motion: reduce) {
            .progress, .check, .file { animation: none !important; }
          }
        `}
        </style>
      </svg>
    </Frame>
  )
}
