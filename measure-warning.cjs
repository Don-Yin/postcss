const { resolve } = require('node:path')
const { execFileSync } = require('node:child_process')

const root = resolve(process.argv[2])
const { parse, Warning } = require(resolve(root, 'lib/postcss.js'))
const fixtures = [
  { name: 'Same-line start', css: 'a b{}', start: { line: 1, column: 3 } },
  { name: 'Multiline start', css: 'a {\n b: c\n}', start: { line: 2, column: 2 } }
]

const cases = fixtures.map(({ name, css, start }) => {
  const warning = new Warning('text', {
    node: parse(css, { from: 'a.css' }).first,
    plugin: 'plugin',
    start
  })
  const match = warning.toString().match(/:(\d+):(\d+): text$/)
  if (!match) throw new Error('Missing diagnostic position')
  return {
    name,
    css,
    requested: start,
    properties: { line: warning.line, column: warning.column },
    formatted: { line: Number(match[1]), column: Number(match[2]) }
  }
})

console.log(JSON.stringify({
  revision: execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(),
  cases
}, null, 2))
