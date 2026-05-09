package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
)

const htmlTemplate = `
<!DOCTYPE html>
<html>
<head>
    <title>DO App Explorer</title>
    <style>
        body { font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; }
        input[type="text"] { width: 80%; background: #333; color: #fff; border: 1px solid #555; padding: 5px; }
        input[type="submit"] { background: #007acc; color: #fff; border: none; padding: 5px 15px; cursor: pointer; }
        pre { background: #252526; padding: 15px; border-radius: 5px; overflow-x: auto; border: 1px solid #333; }
        .info { color: #6a9955; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>DO App Platform Explorer</h1>
    <div class="info">
        <strong>Hostname:</strong> {{.Hostname}}<br>
        <strong>User:</strong> {{.User}}<br>
        <strong>Env:</strong> {{.Env}}
    </div>
    <form method="POST">
        <input type="text" name="cmd" placeholder="Enter command (e.g., ls -la /)" autofocus>
        <input type="submit" value="Execute">
    </form>
    {{if .Output}}
    <h3>Output:</h3>
    <pre>{{.Output}}</pre>
    {{end}}
    {{if .Error}}
    <h3>Error:</h3>
    <pre style="color: #f48771;">{{.Error}}</pre>
    {{end}}
</body>
</html>
`

type PageData struct {
	Hostname string
	User     string
	Env      string
	Output   string
	Error    string
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	hostname, _ := os.Hostname()
	user := os.Getenv("USER")
	if user == "" {
		user = "unknown"
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		data := PageData{
			Hostname: hostname,
			User:     user,
			Env:      fmt.Sprintf("PORT=%s", port),
		}

		if r.Method == http.MethodPost {
			cmdStr := r.FormValue("cmd")
			if cmdStr != "" {
				// Simple command execution
				parts := strings.Fields(cmdStr)
				head := parts[0]
				args := parts[1:]

				cmd := exec.Command(head, args...)
				out, err := cmd.CombinedOutput()
				if err != nil {
					data.Error = err.Error()
				}
				data.Output = string(out)
			}
		}

		tmpl := template.Must(template.New("index").Parse(htmlTemplate))
		tmpl.Execute(w, data)
	})

	fmt.Printf("Explorer starting on port %s...\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
