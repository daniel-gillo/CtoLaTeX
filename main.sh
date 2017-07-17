echo "Starting..."
echo "" > ast.json
$(./c2flow_parser < $1 > ast.json)
python back.py ast.json out.tex
echo "Finished!"
echo "out.tex needs to be compiled using LuaLaTex."