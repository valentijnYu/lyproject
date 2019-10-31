## Semester Project

### Initiate a class

lyman(z,lr,lb,ar,ab,psep,rpb)

	Parameters 
	z Redshift
	lr Line width red
	lb Line width blue
	ar Asym red
	ab Asym blue
	psep separation
	rpb Relative peak flux blue red 


### Functions to generate data

intrinsic_double()
	generate intrinsic fake data
	returns y value 
	x value can read out by self.xx

smooth()
	generate LSF smoothed data
	returns y value 
	x value can read out by self.xx

MuseData()
	generate fake MUSE data
	returns both x and y value with a decreased pixel-scale

MuseDataN(sigma)
	generate fake MUSE data with noise
	returns both x and y value with a decreased pixel-scale
	
	Parameters
	sigma using numpy random normal function with a default sigma value = 3