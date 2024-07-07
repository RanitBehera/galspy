import numpy

class CartesianSightLine:
    def __init__(self,start_pos:tuple[float],end_pos:tuple[float]) -> None:
        self.start_pos  = numpy.array(start_pos)
        self.end_pos    = numpy.array(end_pos)

    def Get_Stops(self,num_stops:int):
        x_stops = numpy.linspace(self.start_pos[0],self.end_pos[0],num_stops)
        y_stops = numpy.linspace(self.start_pos[1],self.end_pos[1],num_stops)
        z_stops = numpy.linspace(self.start_pos[2],self.end_pos[2],num_stops)
        stops   = numpy.array(list(zip(x_stops,y_stops,z_stops)))
        return stops
    
    def Get_Steps(self,step_size:float):
        sightline_length    = numpy.linalg.norm(self.end_pos-self.start_pos)
        sightline_unit_vec  = (self.end_pos-self.start_pos)/sightline_length

        step_lengths = [0]
        while step_lengths[-1]+step_size<=sightline_length:
            step_lengths.append(step_lengths[-1]+step_size)
        step_lengths = numpy.array(step_lengths)

        step_vecs    = numpy.array([sl * sightline_unit_vec for sl in step_lengths])
        steps        = self.start_pos + step_vecs
        return steps


class AngularSightline:
    def __init__(self,from_pos:tuple[float],theta:float,phi:float,max_r:float) -> None:
        self.from_pos   = numpy.array(from_pos)
        self.theta      = theta
        self.phi        = phi
        self.max_r      = max_r
        
    def Get_CartesianSightline(self):
        dx = self.max_r * numpy.sin(self.theta) * numpy.cos(self.phi)
        dy = self.max_r * numpy.sin(self.theta) * numpy.sin(self.phi)
        dz = self.max_r * numpy.cos(self.theta)
        off = numpy.array([dx,dy,dz])
        return CartesianSightLine(self.from_pos,self.from_pos + off)


