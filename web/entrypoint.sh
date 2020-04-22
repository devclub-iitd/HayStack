until curl -f elasticsearch:9200; do
    >&2 echo "Elasticsearch unavailable - sleeping"
    sleep 5
done

flask run --host=0.0.0.0
