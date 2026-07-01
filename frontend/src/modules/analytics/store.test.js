import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAnalyticsStore } from './store'

vi.mock('../../services/api', () => ({
  default: {
    get: vi.fn(),
  },
}))

import api from '../../services/api'

describe('useAnalyticsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('fetchSummary stores response data', async () => {
    api.get.mockResolvedValue({ data: { trend: [] } })
    const store = useAnalyticsStore()

    await store.fetchSummary(14)

    expect(store.summary).toEqual({ trend: [] })
    expect(store.loading).toBe(false)
    expect(store.error).toBe('')
  })
})
