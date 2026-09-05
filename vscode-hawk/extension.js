const vscode = require('vscode');
const path = require('path');
const { spawn } = require('child_process');

let terminalInstance = null;
let diagnosticCollection = null;
let debounceTimer = null;

function getHawkTerminal() {
    let terminal = vscode.window.terminals.find(t => t.name === 'Hawk');
    if (!terminal) {
        terminal = vscode.window.createTerminal({
            name: 'Hawk',
            iconPath: new vscode.ThemeIcon('symbol-event')
        });
    }
    return terminal;
}

function getCliCommand() {
    const home = process.env.HOME || process.env.USERPROFILE || '';
    const cliCandidate = path.join(home, '.pyhawk', 'hawk_cli.py');
    const isWin = process.platform === 'win32';
    const pyBin = isWin ? 'python' : 'python3';
    return { bin: pyBin, cliPath: cliCandidate };
}

function checkDocumentSyntax(document) {
    if (!document) return;
    if (document.languageId !== 'hawk' && !document.fileName.endsWith('.hwk')) {
        return;
    }

    const { bin, cliPath } = getCliCommand();
    const text = document.getText();

    let child;
    try {
        child = spawn(bin, [cliPath, 'check', '--stdin']);
    } catch (e) {
        return;
    }

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', chunk => {
        stdout += chunk;
    });
    child.stderr.on('data', chunk => {
        stderr += chunk;
    });

    child.on('error', err => {
        // Silently ignore if python/pyhawk is unavailable
    });

    child.on('close', code => {
        if (!diagnosticCollection) return;
        try {
            const diags = JSON.parse(stdout);
            const vsDiags = diags.map(d => {
                const line = Math.max(0, (d.line || 1) - 1);
                const col = Math.max(0, (d.col || 1) - 1);
                let endCol = Math.max(col + 1, (d.end_col || (d.col + 5)) - 1);
                
                // Ensure endCol doesn't exceed line length
                try {
                    const lineText = document.lineAt(line).text;
                    endCol = Math.min(lineText.length, Math.max(col + 1, endCol));
                } catch (e) {}

                const range = new vscode.Range(line, col, line, endCol);
                const sev = d.severity === 'warning' ? vscode.DiagnosticSeverity.Warning : vscode.DiagnosticSeverity.Error;
                const diag = new vscode.Diagnostic(range, d.message, sev);
                diag.source = 'PyHawk';
                return diag;
            });
            diagnosticCollection.set(document.uri, vsDiags);
        } catch (e) {
            diagnosticCollection.delete(document.uri);
        }
    });

    child.stdin.write(text);
    child.stdin.end();
}

function scheduleSyntaxCheck(document) {
    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }
    debounceTimer = setTimeout(() => {
        checkDocumentSyntax(document);
    }, 200);
}

function formatHawkDocument(document) {
    return new Promise((resolve) => {
        const { bin, cliPath } = getCliCommand();
        let child;
        try {
            child = spawn(bin, [cliPath, 'format', '--stdin']);
        } catch (e) {
            resolve([]);
            return;
        }

        let stdout = '';
        child.stdout.on('data', chunk => {
            stdout += chunk;
        });

        child.on('error', () => {
            resolve([]);
        });

        child.on('close', code => {
            if (code === 0 && stdout) {
                const fullRange = new vscode.Range(
                    document.positionAt(0),
                    document.positionAt(document.getText().length)
                );
                resolve([vscode.TextEdit.replace(fullRange, stdout)]);
            } else {
                resolve([]);
            }
        });

        child.stdin.write(document.getText());
        child.stdin.end();
    });
}

function activate(context) {
    // 1. Diagnostics collection for red squiggly underlines
    diagnosticCollection = vscode.languages.createDiagnosticCollection('pyhawk');
    context.subscriptions.push(diagnosticCollection);

    // Initial check for all active editors
    if (vscode.window.activeTextEditor) {
        checkDocumentSyntax(vscode.window.activeTextEditor.document);
    }

    // Document event listeners
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => {
            scheduleSyntaxCheck(event.document);
        }),
        vscode.workspace.onDidOpenTextDocument(document => {
            checkDocumentSyntax(document);
        }),
        vscode.workspace.onDidSaveTextDocument(document => {
            checkDocumentSyntax(document);
        }),
        vscode.workspace.onDidCloseTextDocument(document => {
            if (diagnosticCollection) {
                diagnosticCollection.delete(document.uri);
            }
        }),
        vscode.window.onDidChangeActiveTextEditor(editor => {
            if (editor) {
                checkDocumentSyntax(editor.document);
            }
        })
    );

    // 2. Command: Run File (Interpreter)
    let runDisposable = vscode.commands.registerCommand('hawk.runFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('PyHawk: No active file to run.');
            return;
        }

        if (editor.document.isDirty) {
            await editor.document.save();
        }

        const filePath = editor.document.fileName;
        const terminal = getHawkTerminal();
        terminal.show(false);
        terminal.sendText(`pyhawk run "${filePath}"`);
    });

    // 3. Command: Build Native Binary (C99 -O3)
    let buildDisposable = vscode.commands.registerCommand('hawk.buildFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('PyHawk: No active file to compile.');
            return;
        }

        if (editor.document.isDirty) {
            await editor.document.save();
        }

        const filePath = editor.document.fileName;
        const dir = path.dirname(filePath);
        const nameWithoutExt = path.basename(filePath, path.extname(filePath));
        const outBin = path.join(dir, nameWithoutExt);

        const terminal = getHawkTerminal();
        terminal.show(false);
        terminal.sendText(`pyhawk build "${filePath}" && "${outBin}"`);
    });

    // 4. Command: Open REPL
    let replDisposable = vscode.commands.registerCommand('hawk.openRepl', () => {
        const terminal = getHawkTerminal();
        terminal.show(false);
        terminal.sendText('pyhawk repl');
    });

    // 5. Document Formatting Provider (Shift+Option+F / Format Document)
    let formatDisposable = vscode.languages.registerDocumentFormattingEditProvider('hawk', {
        provideDocumentFormattingEdits(document) {
            return formatHawkDocument(document);
        }
    });

    context.subscriptions.push(runDisposable, buildDisposable, replDisposable, formatDisposable);
}

function deactivate() {
    if (diagnosticCollection) {
        diagnosticCollection.clear();
        diagnosticCollection.dispose();
    }
}

module.exports = {
    activate,
    deactivate
};
