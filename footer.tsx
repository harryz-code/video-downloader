import Link from "next/link"

export default function Footer() {
  return (
    <footer role="contentinfo" className="border-t border-zinc-200 bg-white">
      <div className="container mx-auto max-w-6xl px-4 py-10">
        <div className="flex flex-col items-start justify-between gap-6 sm:flex-row sm:items-center">
          <p className="text-sm text-zinc-600">© {new Date().getFullYear()} YT Downloader. All rights reserved.</p>
          <nav aria-label="Legal" className="text-sm">
            <ul className="flex flex-wrap items-center gap-4">
              <li>
                <Link href="#" className="text-zinc-700 hover:text-zinc-900">
                  Terms
                </Link>
              </li>
              <li>
                <Link href="#" className="text-zinc-700 hover:text-zinc-900">
                  Privacy
                </Link>
              </li>
              <li>
                <Link href="#downloader" className="text-zinc-700 hover:text-zinc-900">
                  Start download
                </Link>
              </li>
            </ul>
          </nav>
        </div>
        <p className="mt-4 text-xs text-zinc-500">
          This tool is for personal use only. Ensure you have the right to download the content.
        </p>
      </div>
    </footer>
  )
}
