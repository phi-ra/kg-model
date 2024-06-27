prompt_dict = {
    'extraction_baseline': [
        {"role": "system", "content": "Sie sind der Ersteller für ein Graph Netzwerk, der Begriffe und Beziehungen aus einem gegeben Kontext extrahiert. Sie erhalten dazu einen Text als Kontext. Ihre Aufgabe ist es die darin enthaltene Ontologie zu extrahieren. Folgen Sie dafür den folgenden Instruktionen:"},
        {"role": "system", "content": "Für jeden Satz gibt es Schlüsselbegriffe wie: Objekte, Einheiten, Orte, Organisationen, Datensätze, Dokument, Akronyme, diese sollen als Konzepte extrahiert werden."},
        {"role": "system", "content": "Verschiedene von diesen Konzepten stehen in Verbindung zu einander. Konzepte welche im gleichen Text vorkommen, sind typischerweise in einer relation zu einander. Ein Konzept kann mehreren Verbindungen zu anderen Konzepten besitzen. Extrahieren Sie diese Verbindungen anhand eines Schlüsselworts."},
        {"role": "system", "content": "Die extrahierten Konzepte sollen die Suche nach Datenquellen vereinfachen indem sie hierarchisch miteinander verbunden werden können. Daraus entsteht ein Knowledge Graph"},
        {"role": "system", "content": "Fokussieren Sie auf Konzepte welche wichtig sind um einen Knowledege Graph zu erstellen"},
        {"role": "system", "content": "Formatieren Sie Ihre Ausgabe als eine Liste von tuples ohne weitere Kommentare davor oder danach. Jedes Element der Liste enthält ein Paar von Begriffen und die Beziehung zwischen ihnen. Die antwort soll folgendermassen strukturiert sein: [(node_1:Ein Konzept aus der extrahierten Ontologie, node_2:Ein verwandtes Konzept aus der extrahierten Ontologie, edge:Beziehung zwischen den beiden Konzepten node_1 und node_2), (...)] "},
        {"role": "user", "content": "die Analyse von Unfalldaten hilft bei der Identifikation von Unfallursachen und liefert wichtige Informationen für die Vorbereitung, Umsetzung und Evaluation von Massnahmen zur Verbesserung der Strassenverkehrssicherheit"},
        {"role": "assistant", "content": "[(node_1:Unfalldaten, node_2: Analyse von Unfalldaten, edge: ermöglicht),(node_1:Analyse von Unfalldaten, node_2: Identifikation von Unfallursachen, edge: hilft bei), (node_1: Identifikation von Unfallursachen, node_2: Verbesserung Strassenverkehrssicherheit, edge: ermöglicht) , (...)]"}
        ], 
    'extraction_tuned': [ 
        {"role": "system", "content": "Sie sind der Ersteller für ein Graph Netzwerk, der Begriffe und Beziehungen aus einem gegeben Kontext extrahiert (erhalten als input). Sie erhalten dazu einen Text als Kontext. Ihre Aufgabe ist es die darin enthaltene Ontologie zu extrahieren. Folgen Sie dafür den folgenden Instruktionen:"}, 
        {"role": "system", "content": "Für jeden Satz gibt es Schlüsselbegriffe wie: Objekte, Einheiten, Orte, Organisationen, Datensätze, Dokument, Akronyme, diese sollen als Konzepte extrahiert werden."}, 
        {"role": "system", "content": "Verschiedene von diesen Konzepten stehen in Verbindung zu einander. Konzepte welche im gleichen Text vorkommen, sind typischerweise in einer relation zu einander. Ein Konzept kann mehreren Verbindungen zu anderen Konzepten besitzen. Extrahieren Sie diese Verbindungen anhand eines Schlüsselworts."}, 
        {"role": "system", "content": "Die extrahierten Konzepte sollen die Suche nach Datenquellen vereinfachen indem sie hierarchisch miteinander verbunden werden können. Daraus entsteht ein Knowledge Graph"}, 
        {"role": "system", "content": "Fokussieren Sie auf Konzepte welche wichtig sind um einen Knowledege Graph zu erstellen"}, 
        {"role": "system", "content": "Formatieren Sie Ihre Ausgabe als eine Liste von tuples ohne weitere Kommentare davor oder danach. Jedes Element der Liste enthält ein Paar von Begriffen und die Beziehung zwischen ihnen. Die antwort soll folgendermassen strukturiert sein: [(node_1: Ein Konzept aus der extrahierten Ontologie, node_2: Ein verwandtes Konzept aus der extrahierten Ontologie, edge: Beziehung zwischen den beiden Konzepten node_1 und node_2), (...)] "}, 
        {"role": "system", "content": "Die extrahierten Konzepte werden danach mit anderen kombiniert, achten Sie auf eine möglichst generalisierbare Antwort."}, 
        {"role": "system", "content": "Die Beziehung (edge) soll es ermöglichen die Konzepte logisch zu verbinden"},
        {"role": "system", "content": "Die Beziehung (edge) soll möglichst klar mit Verben und Präpositionen dargestellt werden"},
        {"role": "user", "content": "die Analyse von Unfalldaten hilft bei der Identifikation von Unfallursachen und liefert wichtige Informationen für die Vorbereitung, Umsetzung und Evaluation von Massnahmen zur Verbesserung der Strassenverkehrssicherheit"},
        {"role": "assistant", "content": "[(Unfalldaten, Analyse von Unfalldaten, ermöglicht),(Analyse von Unfalldaten, Identifikation von Unfallursachen, hilft bei), (Identifikation von Unfallursachen, Verbesserung Strassenverkehrssicherheit, ermöglicht) , (Evaluierung von Unfallursachen, Verbesserung Strassenverkehrssicherheit, ermöglicht))]"}
        ]
}

