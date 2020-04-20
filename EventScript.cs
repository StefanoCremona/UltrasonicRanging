using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using System;
using System.IO;

public class EventScript : MonoBehaviour
{
    public Animator myAnimator;
    public Animator secondAnimator;
    public Animator thirdAnimator;
    public GameObject myGameObject;
    public GameObject secondGameObject;
    public GameObject thirdGameObject;
    public bool isThisAnimatorLeading = false;
    private float delta = 0.1f;
    String rootDir = "C:/Users/e7470/rowData";
    public int maxIterations = 10;
    private int iteration = 0;
    public String testName = "testDowglas"; // Change here the name of the test
    private String testDir;

    void Awake() {
        // Print the size of the walking Dowglas
        // Vector3 objectSize = Vector3.Scale(transform.localScale, myGameObject.GetComponentInChildren<Renderer>().bounds.size);
        // print("Size: ");
        // print(objectSize); (1.8, 2.6, 1.2)
        if (!isThisAnimatorLeading) {
            return;
        }
        testDir = "/" + testName;
        if (myAnimator != null && secondAnimator != null) {
            testDir = "/twoDouglasWalking";
        }
        String path = rootDir+testDir;
        if (Directory.Exists(path)) {
            Directory.Delete(path, true);
        }
        DirectoryInfo di = Directory.CreateDirectory(path);
    }

    public void OnAnimationStarts() {
        if (!isThisAnimatorLeading) {
            return;
        }
        print("Animation started");
    }

    String GetTimestamp(DateTime value)
    {
        return value.ToString("yyyyMMddHHmmssffff");
    }

    public void OnAnimationEnds() {
        if (!isThisAnimatorLeading) {
            return;
        }
        String timeStamp = GetTimestamp(DateTime.Now);
        File.Move(rootDir+"/LeftB.txt", rootDir+testDir+"/"+timeStamp+"LeftB.txt"); // Move and recreate the files with points
        File.Move(rootDir+"/RightB.txt", rootDir+testDir+"/"+timeStamp+"RightB.txt");
        File.Move(rootDir+"/LeftM.txt", rootDir+testDir+"/"+timeStamp+"LeftM.txt"); // Move and recreate the files with points
        File.Move(rootDir+"/RightM.txt", rootDir+testDir+"/"+timeStamp+"RightM.txt");
        File.Move(rootDir+"/LeftT.txt", rootDir+testDir+"/"+timeStamp+"LeftT.txt"); // Move and recreate the files with points
        File.Move(rootDir+"/RightT.txt", rootDir+testDir+"/"+timeStamp+"RightT.txt");
        File.Move(rootDir+"/Interceptor.txt", rootDir+testDir+"/"+timeStamp+"Interceptor.txt");
        
        System.IO.File.Create(rootDir+"/LeftB.txt").Dispose();
        System.IO.File.Create(rootDir+"/RightB.txt").Dispose();
        System.IO.File.Create(rootDir+"/LeftM.txt").Dispose();
        System.IO.File.Create(rootDir+"/RightM.txt").Dispose();
        System.IO.File.Create(rootDir+"/LeftT.txt").Dispose();
        System.IO.File.Create(rootDir+"/RightT.txt").Dispose();
        System.IO.File.Create(rootDir+"/Interceptor.txt").Dispose();
        if (iteration >= maxIterations-1) {
            print("Test ended");
            return;
        }
        iteration++;
        if (myAnimator != null)
        {
            float increment = delta * (iteration % 10);
            float rightIncrement = 0;
            if (secondAnimator != null) {
                // If there are 2 gameobjects the first one will move just after 10 iterations
                increment = delta * iteration / 10;
            } else {
                // If there's just 1 gameobject I shift it to the right every 10 iterations
                rightIncrement = delta * iteration / 10;
            }
            // Walking Farward
            // float Z = -8.5f;
            // String animationName = "Standing Walk Forward";
            
            // Normal Walking animation
            float Z = -9.5f;
            String animationName = "Walking10";
            myGameObject.transform.position = new Vector3(-17.96f + rightIncrement, 0f, Z + increment);
            
            myAnimator.Play(animationName, -1, 0f); // Restart Left Douglas walking animation Walking10/Standing Walk Forward
        }
        if (secondAnimator != null)
        {
            //secondAnimator.enabled = false;
            //secondAnimator.enabled = true;
            float increment = delta * (iteration % 10);
            // Test opposite directions
            // secondGameObject.transform.position = new Vector3(-16.84896f, 0f, 0.36f + increment);
            // Test Single Direction
            secondGameObject.transform.position = new Vector3(-16.87f, 0f, -9.95f + increment);
            secondAnimator.Play("Walking2", -1, 0f);
        }
        if (thirdAnimator != null)
        {
            thirdAnimator.enabled = false;
            // myAnimator.Play("Walking10", -1, 0f);
        }
        print("Animation ended");
    }

}
