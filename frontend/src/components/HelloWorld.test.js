import { mount } from '@vue/test-utils'
import { expect, test } from 'vitest'
import HelloWorld from './HelloWorld.vue'

test('HelloWorld component renders message', () => {
  const wrapper = mount(HelloWorld, {
    props: {
      msg: 'Привет, Вестник!'
    }
  })
  expect(wrapper.text()).toContain('Привет, Вестник!')
})

test('HelloWorld component button increments count', async () => {
  const wrapper = mount(HelloWorld)
  const button = wrapper.find('button')
  expect(button.text()).toContain('count is 0')
  await button.trigger('click')
  expect(button.text()).toContain('count is 1')
})
