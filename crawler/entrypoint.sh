until curl -f elasticsearch:9200; do
    >&2 echo "Elasticsearch unavailable - sleeping"
    sleep 5
done

python3 main.py
