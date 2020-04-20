using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using System;
using System.IO;

[RequireComponent(typeof(LineRenderer))]
public class Laser : MonoBehaviour
{
//    public CapsuleCollider playerCollider;
    public UnityEvent OnHitPlayer;
    public String laserSide = "Other"; // 0 Left, 1 Right
    public float range = 50f;
    new public ParticleSystem particleSystem;
    static int arrayLimit = 80;
    // int arrayIndex = 0;
    // int maxLength = 6;
    float[] points = new float[arrayLimit];
    String rootDir = "C:/Users/e7470/rowData/";

    LineRenderer lineRenderer;
    ParticleSystem.ShapeModule shape;
    Vector3 endPoint;

    void Awake()
    {
        if (laserSide == "" || laserSide == null) {
            return;
        }
        File.Create(rootDir+laserSide+".txt").Dispose(); // Creates or recreates the file if it already exists
        
        lineRenderer = GetComponent<LineRenderer>();
        /* if (particleSystem != null)
        {
            shape = particleSystem.shape;
        } */
    }

    void checkPoint(float point) {
        //points[arrayIndex] = point;
        //arrayIndex++;
        //if (arrayIndex == arrayLimit - 1) {
            StreamWriter sw = new StreamWriter(@rootDir+laserSide+".txt", true);
            sw.Write(point);
            sw.Write(",");
            sw.Close();
        //    points = new float[arrayLimit];
        //    arrayIndex = 0;
        //}
    }

    void Update()
    {
        RaycastHit hit;
        endPoint = transform.forward * range;
        //sw.WriteLine(transform.position.ToString() + " " + transform.forward.ToString());
        if (Physics.Raycast(transform.position, transform.forward, out hit, range))
        {
            //sw.WriteLine(transform.position.ToString() + " " + transform.forward.ToString());
            endPoint = transform.InverseTransformPoint(hit.point);
            print(hit.collider.name);
            if ((hit.collider.name.IndexOf("mixamorig") >= 0) || (hit.collider.name == "WallColumn (7)") || (hit.collider.name == "WallStraight (4)")) {
                //print("Beccata Left: " + endPoint.ToString());
                checkPoint(endPoint.z);
            }
           // if (hit.collider == playerCollider)
            //{
                //print("Destra");
                //OnHitPlayer.Invoke();
                //sw.WriteLine(endPoint.ToString());
            //}
        }
        try {
            lineRenderer.SetPosition(1, endPoint);   
        } catch (System.NullReferenceException) {
            print("Exception while redrawing the laser.");
            // throw;
        }
    }

    void OnCollisionEnter(Collision col) {
        print("Collision");
    }
}
