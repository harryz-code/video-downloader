"use client"

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

export default function Faq() {
  return (
    <section id="faq" aria-label="Frequently asked questions" className="border-t border-zinc-200 bg-white">
      <div className="container mx-auto max-w-3xl px-4 py-12 sm:py-16">
        <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">FAQ</h2>
        <p className="mt-3 text-zinc-600">Quick answers to common questions.</p>

        <div className="mt-6">
          <Accordion type="single" collapsible>
            <AccordionItem value="legal">
              <AccordionTrigger>Is this legal?</AccordionTrigger>
              <AccordionContent>
                Download only content you own or have rights to use. Respect YouTube’s Terms and applicable laws.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="cost">
              <AccordionTrigger>Is it really free?</AccordionTrigger>
              <AccordionContent>
                Yes. No signups, no hidden fees. We keep the experience clean and focused.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="quality">
              <AccordionTrigger>Do you support HD and MP3?</AccordionTrigger>
              <AccordionContent>
                Yes, choose common formats such as MP4 and MP3. Availability may depend on the original video.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="privacy">
              <AccordionTrigger>What about privacy?</AccordionTrigger>
              <AccordionContent>We avoid unnecessary tracking. See our Privacy Policy for details.</AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
    </section>
  )
}
