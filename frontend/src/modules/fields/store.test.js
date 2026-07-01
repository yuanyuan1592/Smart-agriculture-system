import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useFieldStore } from './store'

vi.mock('../../services/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}))

import api from '../../services/api'

describe('useFieldStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('fetchFields loads fields and clears error', async () => {
    api.get.mockResolvedValue({ data: [{ id: 1, name: '田1' }] })
    const store = useFieldStore()

    await store.fetchFields()

    expect(store.fields).toHaveLength(1)
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('addField appends the created field', async () => {
    api.post.mockResolvedValue({ data: { id: 2, name: '田2' } })
    const store = useFieldStore()

    const created = await store.addField({ name: '田2' })

    expect(created.name).toBe('田2')
    expect(store.fields).toHaveLength(1)
  })
})
