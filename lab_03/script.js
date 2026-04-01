class Particle{

constructor(x,y,vx,vy,hue){

this.x=x
this.y=y

this.vx=vx
this.vy=vy

this.hue=hue

this.alpha=1
this.decay=0.015

this.active=true
}

update(gravity,canvasHeight){

this.x+=this.vx
this.y+=this.vy

this.vy+=gravity

this.vx*=0.98
this.vy*=0.98

this.alpha-=this.decay

if(this.alpha<=0){
this.active=false
}

if(this.y>=canvasHeight){

this.y=canvasHeight
this.vy*=-0.6

}

}

draw(ctx){

ctx.beginPath()
ctx.arc(this.x,this.y,2,0,Math.PI*2)

ctx.fillStyle=`hsla(${this.hue},100%,50%,${this.alpha})`
ctx.fill()

}

}



class Firework{

constructor(startX,startY,targetX,targetY){

this.x=startX
this.y=startY

this.targetX=targetX
this.targetY=targetY

this.speed=8

const dx=targetX-startX
const dy=targetY-startY
const dist=Math.hypot(dx,dy)

this.vx=(dx/dist)*this.speed
this.vy=(dy/dist)*this.speed

this.hue=Math.random()*360

this.exploded=false
this.active=true
}

update(){

this.x+=this.vx
this.y+=this.vy

const dist=Math.hypot(this.targetX-this.x,this.targetY-this.y)

if(dist<5){

this.exploded=true
this.active=false

}

}

draw(ctx){

ctx.beginPath()
ctx.arc(this.x,this.y,3,0,Math.PI*2)
ctx.fillStyle="white"
ctx.fill()

}

explode(count){

let particles=[]

for(let i=0;i<count;i++){

const angle=Math.random()*Math.PI*2
const speed=Math.random()*5

const vx=Math.cos(angle)*speed
const vy=Math.sin(angle)*speed

const hue=this.hue+(Math.random()*40-20)

particles.push(
new Particle(this.x,this.y,vx,vy,hue)
)

}

return particles

}

}



class FireworkShow{

constructor(canvas){

this.canvas=canvas
this.ctx=canvas.getContext("2d")

this.rockets=[]
this.particles=[]

this.gravity=0.15
this.particleCount=150

this.setupControls()
this.setupEvents()

this.autoTimer=0

this.animate()

}

setupControls(){

const g=document.getElementById("gravitySlider")
const p=document.getElementById("particleSlider")

g.addEventListener("input",()=>{
this.gravity=parseFloat(g.value)
})

p.addEventListener("input",()=>{
this.particleCount=parseInt(p.value)
})

}

setupEvents(){

this.canvas.addEventListener("click",(e)=>{

const rect=this.canvas.getBoundingClientRect()

const x=e.clientX-rect.left
const y=e.clientY-rect.top

this.launch(x,y)

})

}

launch(targetX,targetY){

const startX=this.canvas.width/2
const startY=this.canvas.height

this.rockets.push(
new Firework(startX,startY,targetX,targetY)
)

}

autoLaunch(){

if(Math.random()<0.02){

const x=Math.random()*this.canvas.width
const y=Math.random()*this.canvas.height/2

this.launch(x,y)

}

}

update(){

const ctx=this.ctx

ctx.fillStyle="rgba(0,0,0,0.2)"
ctx.fillRect(0,0,this.canvas.width,this.canvas.height)

ctx.globalCompositeOperation="lighter"

this.autoLaunch()

this.rockets.forEach(r=>{

r.update()
r.draw(ctx)

if(r.exploded){

const newParticles=r.explode(this.particleCount)
this.particles.push(...newParticles)

}

})

this.particles.forEach(p=>{
p.update(this.gravity,this.canvas.height)
p.draw(ctx)
})

this.rockets=this.rockets.filter(r=>r.active)
this.particles=this.particles.filter(p=>p.active)

}

animate(){

const loop=()=>{

this.update()

requestAnimationFrame(loop)

}

loop()

}

}



const canvas=document.getElementById("canvas")

new FireworkShow(canvas)