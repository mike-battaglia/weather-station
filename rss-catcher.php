<?php
/**
 * Plugin Name: RSS Embed Shortcode
 * Description: Provides a [rss_embed feed=""] shortcode to embed RSS feed content.
 * Version: 1.3.1
 * Author: Mike
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

function rss_embed_shortcode($atts) {
    // Parse the shortcode attributes
    $atts = shortcode_atts(
        [
            'feed' => '',
            'max_items' => 5,
            'ul_id' => '',
            'feed_style' => 'default',
        ],
        $atts,
        'rss_embed'
    );

    $feed_url = esc_url($atts['feed']);
    if (empty($feed_url)) {
        return '<p>Please provide a valid feed URL.</p>';
    }

    $rss = fetch_feed($feed_url);
    if (is_wp_error($rss)) {
        error_log('RSS Fetch Error: ' . $rss->get_error_message());
        return '<p>Unable to fetch the RSS feed. Please check the URL.</p>';
    }

    $max_items = intval($atts['max_items']);
    $rss_items = $rss->get_items(0, $max_items);

    if (empty($rss_items)) {
        return '<p style="display:none;">No items found in the feed.</p>';
    }

    $feed_style = esc_attr($atts['feed_style']);

    $ul_id = !empty($atts['ul_id']) ? ' id="' . esc_attr($atts['ul_id']) . '"' : '';
    $output = '<div class="feed-style-' . $feed_style . '"' . $ul_id . '><ul class="rss-embed-list">';
    
    foreach ($rss_items as $item) {
		
		 if (($feed_style == 'reddit')||($feed_style == 'default')) {
            $item_title = esc_html($item->get_title());
            $item_link = esc_url($item->get_permalink());
            $item_content_raw = $item->get_content();
            $item_content_decoded = html_entity_decode($item_content_raw);
            $item_content = wp_kses_post($item_content_decoded);
            $item_date = $item->get_date('Y-m-d H:i:s');

            $output .= '<div class="rss-item">';
            $output .= '<h3><a href="' . $item_link . '">' . $item_title . '</a></h3>';
            $output .= $item_date ? '<p><strong></strong> ' . $item_date . '</p>' : '';
            $output .= '<div class="rss-content">' . $item_content . '</div>';
            $output .= '</div>';
        }
		
		
        if (($feed_style == 'yahoo-sports')||($feed_style == '1')) {
            $item_title = esc_html($item->get_title());
            $item_link = esc_url($item->get_permalink());
            $item_creator = $item->get_item_tags('http://purl.org/dc/elements/1.1/', 'creator') ? esc_html($item->get_item_tags('http://purl.org/dc/elements/1.1/', 'creator')[0]['data']) : '';
            $item_content_encoded = $item->get_item_tags('http://purl.org/rss/1.0/modules/content/', 'encoded') ? wp_kses_post($item->get_item_tags('http://purl.org/rss/1.0/modules/content/', 'encoded')[0]['data']) : '';

            $output .= '<li class="rss-embed-item">';
            $output .= '<h3 class="rss-item-title"><a href="' . $item_link . '" target="_blank" rel="noopener noreferrer">' . $item_title . '</a></h3>';
            $output .= $item_creator ? '<p class="rss-item-creator">By: ' . $item_creator . '</p>' : '';
            $output .= '<div class="rss-item-content-encoded">' . $item_content_encoded . '</div>';
            $output .= '</li>';
        }
		
		if ($feed_style == 'alerts') {
			// Fetch XML feed from the URL using cURL
			$xmlUrl = $feed_url;

			$ch = curl_init();
			curl_setopt($ch, CURLOPT_URL, $xmlUrl);
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
			curl_setopt($ch, CURLOPT_HTTPHEADER, [
				'User-Agent: YourAppName/1.0 (your-email@example.com)'
			]);

			$response = curl_exec($ch);
			$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
			curl_close($ch);

			if ($httpCode !== 200 || !$response) {
				die('Error: Unable to fetch feed. HTTP Code: ' . $httpCode);
			}

			// Load the XML feed from the response
			$xml = simplexml_load_string($response);

			if (!$xml) {
				die('Error: Cannot create object');
			}

			// Register namespaces
			$namespaces = $xml->getNamespaces(true);
			$xml->registerXPathNamespace('default', $namespaces['']);
			$xml->registerXPathNamespace('cap', $namespaces['cap']);

			// Fetch entries from the feed
			$entries = $xml->xpath('//default:entry');

			// Start building the output
			$output .= '<div class="alerts">';

			foreach ($entries as $entry) {
				// Extract data using XPath queries
				$event = $entry->xpath('cap:event')[0] ?? '';

				$link = $entry->xpath('link')[0] ?? '';

				$status = $entry->xpath('cap:status')[0] ?? '';

				$effective = $entry->xpath('cap:effective')[0] ?? '';
				$expires = $entry->xpath('cap:expires')[0] ?? '';
				$urgency = $entry->xpath('cap:urgency')[0] ?? '';
				$severity = $entry->xpath('cap:severity')[0] ?? '';
				$certainty = $entry->xpath('cap:certainty')[0] ?? '';
				$areaDesc = $entry->xpath('cap:areaDesc')[0] ?? '';
				
				// Append the data to the output
				$output .= '<div class="alert">';
				$output .= '<h3><a href="' . htmlspecialchars($link) . '">' . htmlspecialchars($event) . '</a></h3>';
				$output .= ($status !== 'Unknown') ? '<p>Status: ' . htmlspecialchars($status) . '</p>' : '';
				$output .= ($effective !== 'Unknown') ? '<p>Effective: ' . htmlspecialchars($effective) . '</p>' : '';
				$output .= ($expires !== 'Unknown') ? '<p>Expires: ' . htmlspecialchars($expires) . '</p>' : '';
				$output .= ($urgency !== 'Unknown') ? '<p>Urgency: ' . htmlspecialchars($urgency) . '</p>' : '';
				$output .= ($severity !== 'Unknown') ? '<p>Severity: ' . htmlspecialchars($severity) . '</p>' : '';
				$output .= ($certainty !== 'Unknown') ? '<p>Certainty: ' . htmlspecialchars($certainty) . '</p>' : '';
				$output .= ($areaDesc !== 'Unknown') ? '<p>Area: ' . htmlspecialchars($areaDesc) . '</p>' : '';

				$output .= '</div>'; // Close alert div
			}
			$output .= '</div>'; // Close alerts div
		}

		$output .= '</ul></div>';
		return $output;
	}
}

add_shortcode('rss_embed', 'rss_embed_shortcode');
