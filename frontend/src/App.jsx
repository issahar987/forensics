import { useState } from 'react'
// base url backend: http://35.241.231.48:8000/
// button POST Analysis: /send_url
// button POST Preview: /get_preview
// button GET Virus Total Scan: /virus_total_scan
// button GET Clam AntiVirus Scan: /ClamAV_scan
// button GET AST info: /AST_info
function App() {
  const baseUrl = "http://35.241.231.48:8000"
  const [tab, setTab] = useState(null);
  const [url, setUrl] = useState("")
  const [json, setJson] = useState({})
  const [preview, setPreview] = useState(null)

  const analyze = async () => {
    const response = await fetch(`${baseUrl}/send_url?url_to_download=${encodeURIComponent(url)}`, { method: 'POST' })
    const json = await response.json()
    setJson(json);
  }

  const getPreview = async () => {
    const response = await fetch(`${baseUrl}/get_preview?url_to_download=${encodeURIComponent(url)}`, { method: 'POST' })
    const json = await response.json()
    setPreview(json);
  }

  return (
    <main className="flex min-h-screen flex-row items-center justify-between py-4 px-12 w-screen gap-6 bg-zinc-900 h-screen overflow-hidden">
      <div className="flex flex-col w-1/2 gap-4 items-center bg-zinc-800 p-6 rounded-md">
        <input className="p-2 w-full bg-zinc-700 rounded-md" placeholder="Please input URL" value={url} onChange={(e) => setUrl(e.currentTarget.value)} />
        <div className='flex flex-row w-full gap-4'>
          <button className="w-1/2" onClick={getPreview}>Preview</button>
          <button className="w-1/2" onClick={analyze}>Analysis</button>
        </div>
        {preview && <PrettyJson json={preview} />}
      </div>
      <div className="flex flex-col w-1/2 h-full bg-zinc-800 p-6 rounded-md">
        <div className='flex flex-row w-full gap-2'>
          <button disabled={json.results_VT !== undefined ? false : true} className='w-1/3 text-center disabled:opacity-50' onClick={() => setTab(<Tab title="Virus Total Scan" json={json.results_VT}/>)}>Virus Total Scan</button>
          <button disabled={json.results_ClamAV !== undefined ? false : true} className='w-1/3 text-center disabled:opacity-50' onClick={() => setTab(<Tab title="Clam AntiVirus Scan" json={json.results_ClamAV}/>)}>Clam AntiVirus Scan</button>
          <button disabled={json.results_AST !== undefined ? false : true} className='w-1/3 text-center disabled:opacity-50' onClick={() => setTab(<Tab title="AST info" json={json.results_AST}/>)}>AST info</button>
        </div>
        <div id="wrapper" className="">
          { tab ?? null }
        </div>
      </div>
    </main>
  )
}

const Tab = ({title, json}) => {
  return (
    <div className='flex flex-col gap-2 py-2 h-screen'>
      <h2 className='w-full text-center text-lg'>{title}</h2>
      <PrettyJson json={json} />
    </div>
  )
}

const PrettyJson = ({json}) => {
  return (
    <pre className="overflow-scroll h-4/5 bg-zinc-700 rounded-md p-4">
      {JSON.stringify(json, null, 2)}
    </pre>
  )
}

export default App
