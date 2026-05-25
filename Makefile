.PHONY: demo index search context clean

index:
	python -m rag_demo.index --source data/sample_notes

search:
	python -m rag_demo.search "React form typing" --top-k 3

context:
	python -m rag_demo.context "Build a typed React form" --top-k 3

demo: index search context

clean:
	rm -rf .rag_demo rag_demo/__pycache__
