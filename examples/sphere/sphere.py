import numpy as np
from PostMeshPy import PostMeshSurfacePy as PostMeshSurface


def Sphere():

   # THIS IS AN EXAMPLE OF A SPHERE MESHED WITH QUARTIC (P=4)
   # TETRAHEDRAL FINITE ELEMENTS - SAME AS THE C++ EXAMPLE

    # READ MESH DATA
    elements = np.loadtxt("sphere_elements.dat",delimiter=",").astype(np.uint64)
    points = np.loadtxt("sphere_points.dat",delimiter=",",dtype=np.float64)
    edges = np.loadtxt("sphere_edges.dat",delimiter=",").astype(np.uint64)
    faces = np.loadtxt("sphere_faces.dat",delimiter=",").astype(np.uint64)
    # SUPPLY CAD FILE
    iges_filename = "sphere.igs" 

    # DOES THE MESH/CAD FILE NEED TO BE SCALED?
    # THIS IS IMPORTANT AS MOST CAD LIBRARIES SCALE UP/DOWN 
    # IMPORTED CADD FILES
    scale = 1000.;
    # THIS CONDITION TELLS PostMesh IF ALL THE POINTS IN THE MESH
    # FALL WITHIN CAD GEOMETRY OR IF THERE ARE POINST OUTISDE WHICH
    # DO NOT TO BE PROJECTED
    condition = 1.e10;
    # PRECISION TOLERANCE BETWEEN CAD GEOMETRY AND MESH DATA.
    # NORMALLY, DUE TO MESH DATA AND CAD GEOMETRY COMING FROM DIFFERENT
    # SOURCES, THERE'S AN ARITHMATIC PRECISION ISSUE. THIS PRECISION TELLS
    # PostMesh TO TREAT POINTS FROM CAD AND MESH WITHIN THIS PRECISION AS
    # ONE POINT 
    precision = 1.0e-07;
    # NODAL SPACING OF POINTS IN THE REFRERENCE TRIANGLE (GAUSS-LOBATTO SPACING IN THS CASE)
    nodal_spacing = np.loadtxt("nodal_spacing_p4.dat",delimiter=",",dtype=np.float64)

    curvilinear_mesh = PostMeshSurface("tet",3)
    curvilinear_mesh.SetMeshElements(elements)
    curvilinear_mesh.SetMeshPoints(points)
    curvilinear_mesh.SetMeshEdges(edges)
    curvilinear_mesh.SetMeshFaces(faces)
    curvilinear_mesh.SetScale(scale)
    curvilinear_mesh.SetCondition(condition)
    curvilinear_mesh.SetProjectionPrecision(precision)
    curvilinear_mesh.ComputeProjectionCriteria()
    curvilinear_mesh.ScaleMesh()
    curvilinear_mesh.SetNodalSpacing(nodal_spacing)
    # READ THE GEOMETRY FROM THE IGES FILE
    curvilinear_mesh.ReadIGES(iges_filename)
    # EXTRACT GEOMETRY INFORMATION FROM THE IGES FILE
    geometry_points = curvilinear_mesh.GetGeomVertices()
    # curvilinear_mesh.GetGeomEdges()
    curvilinear_mesh.GetGeomFaces()
    curvilinear_mesh.GetGeomPointsOnCorrespondingFaces()
    # FIRST IDENTIFY WHICH SURFACES CONTAIN WHICH FACES
    curvilinear_mesh.IdentifySurfacesContainingFaces()
    # PROJECT ALL BOUNDARY POINTS FROM THE MESH TO THE CURVE
    curvilinear_mesh.ProjectMeshOnSurface()
    # PERFORM POINT INVERSION FOR THE INTERIOR POINTS
    curvilinear_mesh.MeshPointInversionSurface()
    # OBTAIN MODIFIED MESH POINTS - THIS IS NECESSARY TO ENSURE LINEAR MESH IS ALSO CORRECT
    curvilinear_mesh.ReturnModifiedMeshPoints(points)
    # GET DIRICHLET DATA - (THE DISPLACMENT OF BOUNDARY NODES)
    # nodesDBC IS AN ARRAY OF SIZE [NO OF BOUNDARY NODES] CONTAINING 
    # GLOBAL NODE NUMBERS IN THE ELEMENT CONNECTIVITY AND Dirichlet IS 
    # THE CORRESPONDING DISPLACEMENT ARRAY [NO OF BOUNDARY NODES x DIMENSIONS]
    nodesDBC, Dirichlet = curvilinear_mesh.GetDirichletData() 

    print(Dirichlet)


if __name__ == "__main__":
    Sphere()