from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class Paddle(Widget):
	score=NumericProperty(0)
	def BounceBall(self,ball):
		if self.collide_widget(ball):
			vx,vy =ball.velocity
			offset=(ball.center_y -self.center_y) /(self.height/2)
			bounced=Vector(-1 *vx, vy)
			vel =bounced *1.1
			ball.velocity=vel.x ,vel.y  + offset
#adding a ball with  ;
class Ball(Widget):
	#velocity of the ball in the x and y direction
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    #the move func will move the ball one by step in equal interval of time
    def move(self):        
    	self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)
	def ServeBall(self,vel=(7,0)):
		self.ball.center=self.center
		self.ball.velocity=vel
	def update(self,dt):
		self.ball.move()
		#bounce of paddles:
		self.player1.BounceBall(self.ball)
		self.player2.BounceBall(self.ball)
		#bounce off the top and bottom:
		if (self.ball.y<0) or (self.ball.top>self.height):
			self.ball.velocity_y *= -1				
		# updating the score:
		if self.ball.x <self.x:
			self.player2.score +=1
			self.ServeBall(vel=(4,0))
		if self.ball.x > self.width:
			self.player1.score+=1
			self.ServeBall(vel=(-4,0))

	#player control on paddle:
	def on_touch_move(self,touch):
		if touch.x< self.width  / 3:
			self.player1.center_y=touch.y
		if touch.x >self.width -self.width/3:
			self.player2.center_y=touch.y
#initialising the APP :
class PongApp(App):

    def build(self):
        game=PongGame()
        game.ServeBall()
        Clock.schedule_interval(game.update,1.0/60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
