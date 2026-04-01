class Hand{

    constructor(length,width,color){
        this.length = length
        this.width = width
        this.color = color
    }

    draw(ctx,angle){

        ctx.save()

        ctx.rotate(angle)

        ctx.beginPath()
        ctx.moveTo(0,0)
        ctx.lineTo(0,-this.length)

        ctx.lineWidth = this.width
        ctx.strokeStyle = this.color
        ctx.lineCap = "round"

        ctx.stroke()

        ctx.restore()
    }

}



class Clock{

    constructor(canvas){

        this.canvas = canvas
        this.ctx = canvas.getContext("2d")

        this.width = canvas.width
        this.height = canvas.height
        this.radius = this.width/2

        this.paused = false

        this.hourHand = new Hand(this.radius*0.5,6,"black")
        this.minuteHand = new Hand(this.radius*0.75,4,"black")
        this.secondHand = new Hand(this.radius*0.9,2,"red")

        this.animate()
    }


    drawFace(){

        const ctx = this.ctx

        ctx.beginPath()
        ctx.arc(0,0,this.radius*0.95,0,Math.PI*2)
        ctx.lineWidth = 4
        ctx.strokeStyle = "black"
        ctx.stroke()


        for(let i=0;i<60;i++){

            ctx.save()

            ctx.rotate(i*Math.PI/30)

            ctx.beginPath()

            if(i%5===0){
                ctx.moveTo(0,-this.radius*0.85)
                ctx.lineTo(0,-this.radius*0.95)
                ctx.lineWidth=4
            }
            else{
                ctx.moveTo(0,-this.radius*0.9)
                ctx.lineTo(0,-this.radius*0.95)
                ctx.lineWidth=2
            }

            ctx.stroke()

            ctx.restore()
        }

    }


    draw(){

        const ctx = this.ctx

        ctx.clearRect(0,0,this.width,this.height)

        ctx.save()

        ctx.translate(this.width/2,this.height/2)

        ctx.rotate(-Math.PI/2)

        this.drawFace()

        const now = new Date()

        const ms = now.getMilliseconds()
        const sec = now.getSeconds() + ms/1000
        const min = now.getMinutes() + sec/60
        const hr = (now.getHours()%12) + min/60

        const secAngle = sec*Math.PI/30
        const minAngle = min*Math.PI/30
        const hrAngle = hr*Math.PI/6

        this.hourHand.draw(ctx,hrAngle)
        this.minuteHand.draw(ctx,minAngle)
        this.secondHand.draw(ctx,secAngle)

        ctx.restore()

    }


    animate(){

        const loop = ()=>{

            if(!this.paused){
                this.draw()
            }

            requestAnimationFrame(loop)
        }

        loop()
    }

}



const canvas = document.getElementById("clockCanvas")

const clock = new Clock(canvas)



document.addEventListener("keydown",(e)=>{

    if(e.code === "Space"){
        clock.paused = !clock.paused
    }

})