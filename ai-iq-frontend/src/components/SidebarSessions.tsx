import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Badge } from '@/components/ui/badge'

interface SessionItem {
  id: string
  title: string
  date: string
  score?: number
  tier?: 'free' | 'basic' | 'premium'
}

interface Props {
  sessions: SessionItem[]
  onSelect: (id: string) => void
}

export function SidebarSessions({ sessions, onSelect }: Props) {
  return (
    <aside className="h-full w-full border-r border-white/10 bg-black/30">
      <Card className="border-0 bg-transparent">
        <CardHeader>
          <CardTitle className="text-white/90 text-sm">Your Sessions</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <ScrollArea className="h-[calc(100vh-8rem)]">
            <ul className="space-y-1 px-3 pb-3">
              {sessions.map((s) => (
                <li key={s.id}>
                  <button
                    onClick={() => onSelect(s.id)}
                    className="w-full text-left rounded-md px-3 py-2 hover:bg-white/5 focus:bg-white/10"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-white/90 text-sm line-clamp-1">{s.title}</span>
                      {s.score !== undefined && (
                        <Badge variant="secondary" className="ml-2 bg-white/10 text-white/80">
                          {s.score}
                        </Badge>
                      )}
                    </div>
                    <div className="text-xs text-white/50 flex items-center gap-2 mt-1">
                      <span>{s.date}</span>
                      {s.tier && <span className="uppercase">• {s.tier}</span>}
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          </ScrollArea>
        </CardContent>
      </Card>
    </aside>
  )
}
