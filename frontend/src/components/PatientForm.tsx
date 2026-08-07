"use client"
import {useState} from "react"
export default function PatientForm(){
const [symptoms,setSymptoms]=useState("")
async function submit(){
const response =
await fetch(
"/api/triage",
{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
age:45,
sex:"unknown",
oxygen_saturation:95,
symptoms:[
symptoms
]
})
})

const data =
await response.json()
console.log(data)
}

return (
<div>

<h2> Patient Assessment </h2>

<textarea 
placeholder="Describe symptoms" 
value={symptoms} 
onChange={ e=>setSymptoms(e.target.value) }
/>

<button 
onClick={submit}
> Analyze </button>
</div>
)
}