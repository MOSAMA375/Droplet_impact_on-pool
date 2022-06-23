#include "axi.h"
#include "navier-stokes/centered.h"
#define FILTERED 1
#include "two-phase.h"
#include "navier-stokes/conserving.h"
#include "tension.h"
#include "tracer.h"
// #include "view.h"

#define pool -((0.68*L0) - x)
#define Re 1000.
#define We 292.
#define rholiq 1.0
#define rhogas 1.41e-3 
#define muliq (rholiq*U*D/Re)
#define mugas 1.54e-6
#define tensionsurf (rholiq*U*U*D/We)
// #define xc (h+epsilon+D*0.5) 
// #define yc 0.
// #define epsilon (4./pow(2.,level))
#define D 0.2
#define R (D/2.)
#define h (0.2*D)
// #define h (-0.5+0.2*D)
#define U  1.
#define Max_Level 12.

scalar mydrop[], *tracers = {mydrop};

double geometry(double x, double y)
{
    double circle = sq(R)-sq(x-(L0)/2.)-sq(y);
    return circle;
} 
u.n[right]   = dirichlet(0.);
u.n[top]   = dirichlet(0.);
u.n[bottom]   = dirichlet(0.);
u.t[right]   = dirichlet(0.);
u.t[top]   = dirichlet(0.);
u.t[bottom]   = dirichlet(0.);


int main(){
  mu2= mugas; //gas phase
  mu1= muliq; //liquid phase
  rho2= rhogas; //gas phase
  rho1= rholiq;//liquid phase
  f.sigma= tensionsurf;
  TOLERANCE = 1e-4;
  init_grid(1<<8);
  L0=1;
  origin(0.,0.);
  run();
}

event init(i=0){
    if (!restore (file = "restart")) {
    refine(  sq(x-(L0)/2.)+sq(y)>sq(0.8*R)  && sq(x-(L0)/2.)+sq(y)<sq(1.1*R) && level< Max_Level);
    refine(x>=(0.65*L0) &&  x<=(0.73*L0) && level< Max_Level);
    fraction(f , x< (0.68*L0) ? geometry(x,y) : pool);
 
  foreach() {
  		mydrop[] = 0.0;
  	if (sq(R)-sq(x-(L0)/2.)-sq(y) >= 0.)
		{
			mydrop[] = 1.0;
			u.x[] = f[]*U;
		}
		else if (x >= (0.68*L0))
			u.x[] = 0.;
		
  		
    // u.x[]= x <L0/4. ? -f[]*U : 0. ;
	}
    }
}



event logfile (i++) {
  if (i == 0)
    fprintf (stderr,
	     "t dt mgp.i mgpf.i mgu.i grid->tn perf.t perf.speed\n");
  fprintf (stderr, "%g %g %d %d %d %ld %g %g\n", 
	   t, dt, mgp.i, mgpf.i, mgu.i,
	   grid->tn, perf.t, perf.speed);
}

/*
event movie (t += 1e-3)
{
view (quat = {0.000, 0.000, 0.000, 1.000},
      fov = 22, 
      tx = -0.55 , ty =-0.2, //.862, ty = //0.103, 
      width = 1146, height = 840);
squares (color = "u.x", min = -1, max = 1, spread = -1, linear = true);
draw_vof (c = "f");
vectors ();

  scalar omega[];
  vorticity (u, omega);
  view (tx = -0.5);
  clear();
  draw_vof ("f");
  squares ("omega", linear = true, spread = 10);
  box ();
  save ("movie1.mp4");
}
*/

event snapshot (t = 0.1; t += 0.1; t <= 10) {
  char name[80];
  sprintf (name, "snapshot-%g", t);
  scalar pid[];
  foreach()
    pid[] = fmod(pid()*(npe() + 37), npe());
  boundary ({pid});
  dump (name);
}

event snap (t = 0.;t += 1e-3 ; t <= 10) {
  char name[80];
  sprintf (name, "snapshot-%3.3f.gfs", t);
  scalar omega[];
  vorticity (u, omega);
 output_gfs (file = name, t = t, list = {f,u,p,omega,mydrop});
 sprintf (name, "restart");
 dump (name);
}

event adapt(i++)
{
double uemax = 0.1*normf(u.x).avg;
  scalar f1[], kappa[];
  foreach()
    f1[] = f[];
  boundary ({f1});
//  scalar omega[];
//  vorticity (u, omega);
//  double oemax = 0.2*normf(omega).avg;
  curvature (f1, kappa, sigma = 0.);
  adapt_wavelet ({f1,u,kappa}, (double[]){1e-4,uemax,uemax,1e-2}, minlevel = 5, maxlevel = Max_Level);

}




